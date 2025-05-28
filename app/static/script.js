async function submitImage() {
  const token = document.getElementById("tokenInput").value.trim();
  const fileInput = document.getElementById("imageInput");
  const resultBox = document.getElementById("result");

  resultBox.classList.remove("hidden");
  resultBox.textContent = "Sending image for moderation...";

  if (!token || fileInput.files.length === 0) {
    resultBox.textContent = "Please provide both a token and an image.";
    return;
  }

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/moderate", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: formData
    });

    const data = await res.json();
    console.log("MODERATION RESULT:", data);

    if (!res.ok) {
      resultBox.textContent = `❌ Error: ${data.detail || res.statusText}`;
      return;
    }

    let output = `📝 Filename: ${data.filename}\n`;
    output += `✅ Safe: ${data.safe ? "Yes" : "❌ No"}\n\n`;
    output += `📊 Categories:\n`;

    if (Array.isArray(data.categories) && data.categories.length > 0) {
      data.categories.forEach(cat => {
        output += `- ${cat.label}: ${(cat.confidence * 100).toFixed(1)}%\n`;
      });
    } else {
      output += "No content flags detected.";
    }

    resultBox.textContent = output;

  } catch (err) {
    console.error("Error during fetch:", err);
    resultBox.textContent = "Unexpected error. See console for details.";
  }
}
