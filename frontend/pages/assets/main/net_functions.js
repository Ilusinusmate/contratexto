export async function setName(name, connection_id) {
  let url = new URLSearchParams();
  url.append("new_nickname", name);
  url.append("connection_id", connection_id);
  const response = await fetch(
    `${window.location.origin}/set-name/?${url.toString()}`,
    {
      method: "POST",
    }
  );

  const data = response.json();
  return data["error"];
}

export async function getWordPos(word, connection_id) {
  let url = new URLSearchParams();
  url.append("word", word);
  url.append("connection_id", connection_id);
  const response = await fetch(
    `${window.location.origin}/words/?${url.toString()}`,
    {
      method: "GET",
    }
  );

  const data = await response.json();
  if (data["type"] === "ERROR") {
    console.error(data["error"]);
  }
  console.log(data);
  return data["position"];
}

export async function askHint(connection_id) {
  let url = new URLSearchParams();
  url.append("connection_id", connection_id);
  const response = await fetch(
    `${window.location.origin}/ask-hint/?${url.toString()}`,
    {
      method: "GET",
    }
  );

  return await response.json();
}