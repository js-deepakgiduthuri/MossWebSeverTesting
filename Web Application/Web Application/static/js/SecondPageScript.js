function openTab(evt, optionName) {
  var i, tabcontent, tablinks;

  // Hide all tab content
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Remove 'active' class from all tab links
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the selected tab content and set 'active' class to the button that opened the tab
  document.getElementById(optionName).style.display = "flex";
  evt.currentTarget.className += " active";

  if (optionName === "State") {
    // Fetch the JSON data
    fetch('/static/data.json')
      .then(response => response.json())
      .then(data => displayStateParams(data))
      .catch(error => console.log(error));
  }

  if (optionName === "APNs") {
    // Fetch the available APNs
    fetch('/get_apn')
      .then(response => response.json())
      .then(data => populateApnDropdown(data))
      .catch(error => console.log(error));
  }
}

// Wait for the document to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
  // Get the input elements for the IP address
  var ipAddressSelect = document.getElementById("ip-address-type");
  var ipAddressInput = document.getElementById("ip-address");
  var subnetMaskInput = document.getElementById("subnet-mask");
  var gatewayInput = document.getElementById("gateway");
  var dnsServerInput = document.getElementById("dns-server");
  var dnsSecondaryInput = document.getElementById("dns-secondary");

  // Add event listener to the IP address select dropdown
  ipAddressSelect.addEventListener("change", function() {
    var selectedOption = ipAddressSelect.value;
    if (selectedOption === "dynamic") {
      ipAddressInput.disabled = true;
      subnetMaskInput.disabled = true;
      gatewayInput.disabled = true;
      dnsServerInput.disabled = true;
      dnsSecondaryInput.disabled = true;
    } else {
      ipAddressInput.disabled = false;
      subnetMaskInput.disabled = false;
      gatewayInput.disabled = false;
      dnsServerInput.disabled = false;
      dnsSecondaryInput.disabled = false;
    }
  });

  // Add event listener for the "Add APN" button
  var addApnButton = document.getElementById("add-apn");
  if (addApnButton) {
    addApnButton.addEventListener("click", function() {
      // Redirect to the 'add_apn.html' page
      window.location.href = "/add_apn";
    });
  }

  // Add event listener for the "Remove APN" button
  var removeApnButton = document.getElementById("remove-apn");
  if (removeApnButton) {
    removeApnButton.addEventListener("click", function() {
      // Redirect to the 'remove_apn.html' page
      window.location.href = "/remove_apn";
    });
  }
});

function displayStateParams(data) {
  var stateParamsContainer = document.getElementById("stateParamsContainer");

  // Clear existing content
  stateParamsContainer.innerHTML = "";

  // Create a title for the parameters
  var paramsTitle = document.createElement("h2");
  paramsTitle.textContent = "State Parameters";
  stateParamsContainer.appendChild(paramsTitle);

  // Loop through the parameters and create labels and values
  for (var key in data) {
    var label = document.createElement("label");
    label.classList.add("param-label");
    label.textContent = key + ":";
    stateParamsContainer.appendChild(label);

    var value = document.createElement("span");
    value.classList.add("param-value");
    var paramValue = data[key];

    if (typeof paramValue === "object") {
      // Handle nested objects, like the 'endpoint' object
      value.textContent = JSON.stringify(paramValue);
    } else {
      value.textContent = " " + paramValue; // Add a space before the parameter value
    }

    stateParamsContainer.appendChild(value);

    var lineBreak = document.createElement("br");
    stateParamsContainer.appendChild(lineBreak);
  }
}

function populateApnDropdown(apnData) {
  var apnDropdown = document.getElementById("apn-dropdown");

  // Clear existing options
  apnDropdown.innerHTML = "";

  // Populate dropdown with APN data
  for (var key in apnData) {
    var option = document.createElement("option");
    option.value = key;
    option.textContent = key + ": " + apnData[key];
    apnDropdown.appendChild(option);
  }
}

