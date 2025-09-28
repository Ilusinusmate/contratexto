import { createNode, GameRank } from "./ranks.js";
import { setName, getWordPos, askHint } from "./net_functions.js";

const show_hints = document.getElementById("show_hints");
const skills = { number: 3 };
show_hints.textContent = `Congelar/Dicas: ${skills.number}`;

class Game {
  constructor(connection_id, username) {
    this.input = document.getElementById("word_input");
    this.guesses = document.getElementById("guesses");
    this.hintButton = document.getElementById("hint_button");
    this.gamerank = new GameRank();
    this.connection_id = connection_id;
    this.username = username;

    this.used_words = new Set();
    this.position_list = [];
    this.hasAlert = false;
    this.minPos = 1000000;

    this.input.addEventListener(
      "keydown",
      async (event) => await this.handleEnter(event)
    );
    this.hintButton.addEventListener(
      "click",
      async () => await this.handleClick()
    );
  }

  async handleClick() {
    if (this.minPos <= 2) {
      this.createWarning("Você não pode mais pedir Dicas");
      return;
    }

    const data = await askHint(this.connection_id);
    if (data["type"] === "ERROR") {
      this.createWarning(data["error"]);
      return;
    }

    skills.number--;
    const show_hints = document.getElementById("show_hints");
    show_hints.textContent = `Congelar/Dicas: ${skills.number}`;

    const word = data["word"];
    const position = data["position"];

    this.show(word, position, this.guesses.firstElementChild);
    this.gamerank.matchCondition.get(this.username).setPoints(position);
    this.gamerank.uploadActualRank();
  }

  async handleEnter(event) {
    if (event.key !== "Enter") return;
    event.preventDefault();

    const actual_w = this.input.value.trim();

    if (!actual_w) return;

    this.input.value = "";

    if (this.checkAlert(actual_w)) return;

    this.used_words.add(actual_w);

    const position = await getWordPos(actual_w, this.connection_id); // isso aqui é basicamente um teste a api vai me retornar isso

    if (position === null) {
      this.createWarning("Palavra desconhecida!");
      return;
    }

    this.insertPosition(actual_w, position);
  }

  setUser(name, points = 0) {
    this.gamerank.setUser(name, skills, points);
  }

  insertPosition(actual_w, wordPosition) {
    if (wordPosition <= 1) {
      this.gamerank.finishMatch(this.username);
      this.guesses.innerHTML = "";
      this.minPos = 1000000;
      this.used_words.clear();
      this.hasAlert = false;
      skills.number = 3;
      document.getElementById(
        "show_hints"
      ).textContent = `Congelar/Dicas: ${skills.number}`;
      this.createWarning(`o jogador ${this.username} venceu a rodada.`);
      return;
    }
    if (wordPosition < this.minPos) {
      const playerObj = this.gamerank.matchCondition.get(this.username);
      if (playerObj) {
        playerObj.setPoints(wordPosition);
        this.gamerank.uploadActualRank();
        this.minPos = wordPosition;
      }
    }

    const existingGuesses = Array.from(
      this.guesses.querySelectorAll("li.guess")
    );
    const DOM_pos = existingGuesses.find(
      (li) => Number(li.dataset.pos) > wordPosition
    );

    this.show(actual_w, wordPosition, DOM_pos);
  }

  show(actual_w, wordPosition, DOM_pos = null) {
    const l1 = createNode("li", "guess");
    l1.dataset.pos = String(wordPosition);

    const color_percent = this.widthFormat(wordPosition);
    const percentDiv = createNode("div", "percent");
    const wordSpan = createNode("span", "front_word", actual_w);
    const posSpan = createNode("span", "front_word", wordPosition);

    percentDiv.style.width = color_percent + "%";
    percentDiv.style.backgroundColor = this.choose_color(color_percent);

    l1.appendChild(percentDiv);
    l1.appendChild(wordSpan);
    l1.appendChild(posSpan);

    if (DOM_pos) this.guesses.insertBefore(l1, DOM_pos);
    else this.guesses.appendChild(l1);
  }

  widthFormat(value) {
    const normalized = (value - 1) / (20000 - 1);
    return (1 - Math.sqrt(normalized)) * 100;
  }

  choose_color(percent) {
    if (percent <= 33.3) return "#f91880";
    if (percent <= 67) return "#ef7d31";
    return "#00ba7c";
  }

  createWarning(msg) {
    if (!this.hasAlert) {
      this.guesses.prepend(createNode("li", "warning", msg));
      this.hasAlert = true;
    } else {
      const first = this.guesses.firstElementChild;
      if (first.textContent !== msg) {
        first.textContent = msg;
      }
    }
  }

  checkAlert(actual_w) {
    if (this.hasAlert) {
      this.guesses.firstElementChild?.remove();
      this.hasAlert = false;
    }

    if (this.used_words.has(actual_w)) {
      this.createWarning("Você já digitou essa palavra.");
      return true;
    }
    if (actual_w.includes(" ")) {
      this.createWarning("Não é permitido palavras com espaço.");
      return true;
    }
    if (!/^[A-Za-zÀ-ÿ]+$/.test(actual_w)) {
      this.createWarning("Não é permitido caracteres especiais.");
      return true;
    }

    return false;
  }
}

async function initialize(connection_id, username, game) {
  const error = await setName(username, connection_id);

  if (error) {
    window.alert(error);
    game.createWarning(error);
    window.location.href = "/";
  }

  game.setUser(username);
}

document.addEventListener("DOMContentLoaded", async (e) => {
  const socket = new WebSocket(`ws://${window.location.host}/ws`);
  const username = sessionStorage.getItem("username");
  let game;

  socket.addEventListener("message", async (event) => {
    try {
      const data = JSON.parse(event.data);
      const connection_id = data["connection_id"];
      sessionStorage.setItem("connection_id", connection_id);
      console.log(data);
      
      if (game === undefined) {
        game = new Game(connection_id, username);
      }


      if (data["type"] === "LOGIN") {
        await initialize(connection_id, username, game);
        return;
      }

    } catch (err) {
      console.error("Received non-JSON message:", event.data);
    }
  });
});
