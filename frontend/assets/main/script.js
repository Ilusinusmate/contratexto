import { createNode, GameRank } from "./ranks.js";

const show_hints = document.getElementById("show_hints");
const skills = {number : 3};
show_hints.textContent = `Congelar/Dicas: ${skills.number}`;

class Game {
  constructor() {
    this.input = document.getElementById("word_input");
    this.guesses = document.getElementById("guesses");
    this.hintButton = document.getElementById("hint_button");
    this.gamerank = new GameRank();

    this.used_words = new Set();
    this.position_list = [];
    this.hasAlert = false;
    this.minPos = 1000000;

    this.input.addEventListener("keydown", (event) => this.handleEnter(event));
    this.hintButton.addEventListener("click", () => this.handleClick());
  }

  handleClick() {
    if (this.minPos <= 2){
      this.createWarning("Você não pode mais pedir Dicas");
      return;
    } 
    if (this.minPos == 1000000) return;

    if (skills.number <= 0) return;
    
    const position = Math.floor(this.minPos / 2);
    
    this.minPos = position;
    skills.number--;

    this.gamerank.matchCondition.get(username).setPoints(position);
    this.gamerank.uploadActualRank();
    
    const show_hints = document.getElementById("show_hints"); 
    show_hints.textContent = `Congelar/Dicas: ${skills.number}`;
    
    const actual_w = "Pegar na API"; 

    this.show(actual_w, position, this.guesses.firstElementChild);
  }

  handleEnter(event) {
    if (event.key !== "Enter") return;
    event.preventDefault();

    const actual_w = this.input.value.trim();

    if (!actual_w) return;

    this.input.value = "";

    if (this.checkAlert(actual_w)) return;

    this.used_words.add(actual_w);

    const position = Math.floor(Math.random() * 10);  // isso aqui é basicamente um teste a api vai me retornar isso

    this.insertPosition(actual_w, position);
  }

  setUser(name, points = 0) {
    this.gamerank.setUser(name, skills, points);
  }

  insertPosition(actual_w, wordPosition) {
    if (wordPosition <= 1) {
        this.gamerank.finishMatch(username);
        this.guesses.innerHTML = "";
        this.minPos = 1000000;
        this.used_words.clear();
        this.hasAlert = false;
        skills.number = 3;
        document.getElementById("show_hints").textContent = `Congelar/Dicas: ${skills.number}`;
        this.createWarning(`o jogador ${username} venceu a rodada.`)
        return;
    } 
    if (wordPosition < this.minPos) {
        const playerObj = this.gamerank.matchCondition.get(username);
        if (playerObj) {
            playerObj.setPoints(wordPosition);
            this.gamerank.uploadActualRank();
            this.minPos = wordPosition;
        }
    }

    const existingGuesses = Array.from(this.guesses.querySelectorAll('li.guess'));
    const DOM_pos = existingGuesses.find(li => Number(li.dataset.pos) > wordPosition);

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

const username = sessionStorage.getItem("username");
const game = new Game();
game.setUser(username);