async function sendVent() {
    const input = document.getElementById('ventInput');
    const statusMessage = document.getElementById('statusMessage');
    const text = input.value.trim();

    if (!text) return;

    try {
        // Asegúrate de que esta URL coincida con la que expone tu Docker (8000)
        const response = await fetch('http://localhost:8000/api/vent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        if (response.ok) {
            input.value = ''; // Limpiar la caja
            statusMessage.textContent = 'Desahogo asegurado en la bóveda. Se autodestruirá pronto.';
            statusMessage.className = 'success';
        } else {
            throw new Error('Error al guardar');
        }
    } catch (error) {
        statusMessage.textContent = 'Hubo un error al conectar con la bóveda.';
        statusMessage.className = 'error';
    }
}