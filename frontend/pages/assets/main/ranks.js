import { freezePlayer } from "./net_functions.js";

export function createNode(tag, fClass, content = null) {
  const node = document.createElement(tag);
  node.classList.add(fClass);
  node.textContent = content;
  return node;
}

function uploadRank(map, containerId) {
  const sortPlayers = (map) =>
      [...map.values()].sort((a, b) => a.points - b.points);

  const reorder = (container, players) => {
    let last = null;
    for (const player of players) {
      const li = player.li;
      if (!last) {
        if (container.firstChild !== li) container.insertBefore(li, container.firstChild);
      } else {
        if (last.nextSibling !== li) container.insertBefore(li, last.nextSibling);
      }
      last = li;
    }
  };

  reorder(document.getElementById(containerId), sortPlayers(map));
}

const matchCondition = new Map(); 
const gameCondition = new Map(); 

export class GameRank {
  constructor() {
    this.matchCondition = matchCondition; 
    this.gameCondition = gameCondition; 
  }

  setUser(name, connection_id, nSkills, currentPlayerId) {
    const actualPlayer = new ActualPlayer(name, connection_id, nSkills, currentPlayerId);
    this.matchCondition.set(connection_id, actualPlayer);

    const gamePlayer = new GamePlayer(name, connection_id);
    this.gameCondition.set(connection_id, gamePlayer);
  }

  uploadGameRank() {
    uploadRank(this.gameCondition, "game_rank");
  }

  uploadActualRank() {
    uploadRank(this.matchCondition, "actual_rank");
  }

  deleteUser(connection_id) {
    this.matchCondition.delete(connection_id);
    this.gameCondition.delete(connection_id);
  }

  finishMatch(username) {
    const winner = this.gameCondition.get(username);
    if (winner) {
      const points = winner.addPoints(1);
      if (points == 5){
        alert(`O jogador ${username} venceu o jogo!`);
        this.resetGame();
      }
    }
    for (const player of this.matchCondition.values()) {
      player.setPoints(0);
    }

    this.uploadGameRank();
  }
}

class GamePlayer {
  constructor(name, connection_id) {
    this.frontRank = document.getElementById("game_rank");

    this.name = name;
    this.connection_id = connection_id;
    this.points = 0;

    this.show();
  }

  show() {
    this.li = createNode("li", "position");
    this.li.style.backgroundColor = "#1e2732";

    this.spanName = createNode("span", "front_word", this.name);
    this.spanPoints = createNode("span", "front_word", this.points);

    this.li.appendChild(this.spanName);
    this.li.appendChild(this.spanPoints);

    this.frontRank.appendChild(this.li);
  }

  setName(newName) {
    this.name = newName;
    this.spanName.textContent = newName;
  }

  addPoints(newPoints) {
    this.points += newPoints;
    this.spanPoints.textContent = this.points;
    return this.points;
  }
}

class ActualPlayer {
  constructor(name, connection_id, skills, currentPlayerId) {
    this.frontRank = document.getElementById("actual_rank");

    this.name = name;                 
    this.connection_id = connection_id; 
    this.skills = skills;               
    this.currentPlayerId = currentPlayerId; 
    this.points = 0;
    this.is_frozen = false;

    this.show();
  }

  show() {
    this.li = createNode("li", "position");
    this.li.style.backgroundColor = "#1e2732";

    this.div_button = createNode("div", "div_button");

    this.spanName = createNode("span", "front_word", this.name);
    this.spanPoints = createNode("span", "front_word", this.points);

    this.createFreezeButton();

    this.div_button.appendChild(this.freezeButton);
    this.div_button.appendChild(this.spanName);

    this.li.appendChild(this.div_button);
    this.li.appendChild(this.spanPoints);

    this.frontRank.appendChild(this.li);
  }

  setPoints(newPoints) {
    this.points = newPoints;
    this.spanPoints.textContent = newPoints;
  }

  setName(newName) {
    this.name = newName;
    this.spanName.textContent = newName;
  }

  setFrozen(state){
    this.is_frozen = state;
  }

  createFreezeButton() {
    this.freezeButton = createNode("button", "freeze_button", "🧊");

    this.freezeButton.addEventListener("click", () => {
      const clickedBy = this.currentPlayerId;   
      const target = this.connection_id;       

      if (this.skills.number <= 0) return;
      if (this.freezeButton.classList.contains("pressed")) return;
      if (this.is_frozen) return;

      const data = freezePlayer(target, clickedBy);
      if (data["type"] === "ERROR") {
        console.error(data["error"]);
        return;
      }

      matchCondition.get(target).setFrozen(true);

      this.skills.number--;
      document.getElementById("show_hints").textContent = `Congelar/Dicas: ${this.skills.number}`;

      this.freezeButton.classList.add("pressed");

      setTimeout(() => {
        matchCondition.get(target).setFrozen(false);
        this.freezeButton.classList.remove("pressed");
      }, 20000);
    });
  }
}
