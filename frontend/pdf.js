function generatePDF(content) {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();
  const lines = doc.splitTextToSize(content || document.getElementById("chat-box").innerText, 180);
  let y = 20;
  lines.forEach(line => {
    doc.text(15, y, line);
    y += 7;
  });
  doc.save("resume.pdf");
}