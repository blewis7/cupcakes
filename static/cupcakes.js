const BASE_URL = 'http://127.0.0.1:5000/api';

function generateCupcakeHTML(cupcake){
    return `
        <div data-cupcake-id=${cupcake.id}>
            <li>
                ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
                <button class="delete-button">X</button>
            </li>
            <img class="cupcake-img" src="${cupcake.image}">
        </div>
    `;
}


async function showCupcakesOnPage(){
    const response = await axios.get(`${BASE_URL}/cupcakes`);
    for (let cupcake of response.data.cupcakes){
        let newCupcake = $(generateCupcakeHTML(cupcake));
        $('#cupcake-list').append(newCupcake);
    }
}


$("#new-cupcake-form").on("submit", async function (e){
    e.preventDefault();

    let flavor = $("#form-flavor").val();
    let size = $("#form-size").val();
    let rating = $("#form-rating").val();
    let image = $("#form-image").val();

    const newCupcakeRes = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        size,
        rating,
        image
    });

    let newCupcake = $(generateCupcakeHTML(newCupcakeRes.data.cupcake));
    $('#cupcake-list').append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});


$("#cupcake-list").on("click", ".delete-button", async function (e){
    e.preventDefault();

    let $cupcake = $(e.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});


$(showCupcakesOnPage);