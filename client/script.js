window.onload = function () {
    fetch("http://127.0.0.1:5000/get_location_names")
        .then(response => response.json())
        .then(data => {
            let locationSelect = document.getElementById("location");
            data.locations.forEach(loc => {
                let option = document.createElement("option");
                option.value = loc;
                option.text = loc;
                locationSelect.appendChild(option);
            });
        });
};

document.getElementById("priceForm").addEventListener("submit", function (e) {
    e.preventDefault();

    let sqft = document.getElementById("area").value;
    let bhk = document.getElementById("bhk").value;
    let bath = document.getElementById("bath").value;
    let location = document.getElementById("location").value;

    let formData = new FormData();
    formData.append("total_sqft", sqft);
    formData.append("bhk", bhk);
    formData.append("bath", bath);
    formData.append("location", location);

    fetch("http://127.0.0.1:5000/predict_home_price", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("price").innerText =
                "₹ " + data.estimated_price + " Lakhs";
        });
});
