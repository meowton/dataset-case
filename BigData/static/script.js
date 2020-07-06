getFormMethod = (form, method) => {
  document.getElementById(form).method = method;
};

setElementValue = (element, value) => {
  document.getElementById(element).value = value
};

downloadCSV = (csv, filename) => {
  let csvFile, link;
  // CSV file
  csvFile = new Blob([csv], {type: "text/csv"});
  // Download link
  link = document.createElement("a");
  // File name
  link.download = filename;
  // Create a link to the file
  link.href = window.URL.createObjectURL(csvFile);
  // Hide download link
  link.style.display = "none";
  // Add the link to DOM
  document.body.appendChild(link);
  // Click download link
  link.click();
};

exportTableToCSV = (filename) => {
  let csv = [];
  let rows = document.querySelectorAll("table tr");

  for (let i = 0; i < rows.length; i++) {
    let row = [], cols = rows[i].querySelectorAll("td, th");
    for (let j = 0; j < cols.length; j++)
      row.push(cols[j].innerText);
    csv.push(row.join(","));
  }
  // Download CSV file
  downloadCSV(csv.join("\n"), filename);
};
