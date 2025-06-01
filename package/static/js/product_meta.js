document.addEventListener("DOMContentLoaded", () => {
  const statusDiv = document.getElementById("meta-status");
  const form = document.getElementById("meta-form");

  async function fetchMeta() {
    try {
      const res = await fetch(`/api/meta/${productId}`);
      if (!res.ok) throw new Error("No metadata found");
      const data = await res.json();
      fillForm(data);
      statusDiv.textContent = "Metadata loaded.";
      form.classList.remove("hidden");
    } catch (err) {
      statusDiv.textContent = "No metadata found. You can add new metadata.";
      form.classList.remove("hidden");
    }
  }

  function fillForm(data) {
    document.getElementById("tags").value = Array.isArray(data.tags) 
    ? data.tags.join(", ") 
    : "";
    document.getElementById("specifications").value = data.specifications && typeof data.specifications === 'object'
    ? Object.entries(data.specifications)
        .map(([k, v]) => `${k}: ${v}`)
        .join("\n")
    : "";
    document.getElementById("care_instructions").value = data.care_instructions || "";
    document.getElementById("seo_title").value = data.seo_title || "";
    document.getElementById("seo_description").value = data.seo_description || "";
    document.getElementById("vendor_notes").value = data.vendor_notes || "";
  }

  document.getElementById("save-meta").addEventListener("click", async () => {
    const payload = {
      tags: document.getElementById("tags").value.split(",").map(s => s.trim()).filter(Boolean),
      specifications: Object.fromEntries(
        document.getElementById("specifications").value
          .split("\n")
          .map(line => line.split(":").map(s => s.trim()))
          .filter(([k, v]) => k && v)
      ),
      care_instructions: document.getElementById("care_instructions").value,
      seo_title: document.getElementById("seo_title").value,
      seo_description: document.getElementById("seo_description").value,
      vendor_notes: document.getElementById("vendor_notes").value
    };

    const res = await fetch(`/api/meta/${productId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      alert("Metadata saved successfully");
    } else {
      alert("Failed to save metadata");
    }
  });

  document.getElementById("cancel-meta").addEventListener("click", () => {
    fetchMeta(); // Revert changes
  });

  document.getElementById("cancel-meta").addEventListener("click", () => {
  if (confirm("Are you sure you want to discard changes?")) {
      window.history.back();
    }
  });

  fetchMeta();
});
