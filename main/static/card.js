document.addEventListener("DOMContentLoaded", () => {
    //const cardForm = document.getElementById("cardForm");
    const resultDiv = document.getElementById('results');
    // si el formulario envio algo
    document.getElementById("cardForm").addEventListener("submit", async (event) => {
        // evitar que cargue la pagina
        event.preventDefault();

        // limpiar el resultado anterior
        resultDiv.innerHTML = '';

        // obtener el input
        const cardNumber = document.getElementById("card_number").value;
        console.log("A: " +cardNumber);

        try {
            const response = await fetch('/validate_card', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'card_number': cardNumber
                })
            });
            console.log("Response: " +response);
            const data = await response.json();
            console.log("Data: " +data);

            // mostrar resultados
            
            // si la peticion se hizo correctamente
            if (data.success) {
                const binInfo = data.BIN;
                resultDiv.innerHTML = `
                    <h2>Detalles de la tarjeta</h2>
                    <p>Valid: ${binInfo.valid}</p>
                    <p>Tipo: ${binInfo.scheme}</p>
                    <p>Pais: ${binInfo.country.country}</p>
                `
            }
            // si no se hizo correctamente
            else {
                console.log(data);
                resultDiv.innerHTML = `<p>Hubo un error</p>`;
            }
        } catch (error) {
            console.error("El error fue: " + error);

            document.getElementById('results').innerHTML = `<p> ${error.message} </p>`;
        }
    });
});