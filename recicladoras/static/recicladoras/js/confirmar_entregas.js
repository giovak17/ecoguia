function cargarMateriales(puntoId, materialSelect) {
    fetch(`get-materiales/${puntoId}/`)
        .then(response => response.json())
        .then(data => {
            materialSelect.innerHTML = '';
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.id;
                option.textContent = item.nombre;
                materialSelect.appendChild(option);
            });
        });
}

function agregarMaterial() {
    const contenedor = document.getElementById('materiales-container');
    const puntoId = document.getElementById('punto_entrega').value;
    if (!puntoId) {
        alert("Primero selecciona un punto de reciclaje.");
        return;
    }

    const grupo = document.createElement('div');
    grupo.className = 'grupo-material';

    // grupo.innerHTML = `
    //     <hr>
    //     <label>Tipo de Material:</label><br>
    //     <select name="material[]" required></select><br><br>

    //     <label>Cantidad:</label><br>
    //     <input type="number" name="cantidad[]" min="1" required><br><br>

    //     <label>Condiciones de Entrega:</label><br>
    //     <textarea name="condiciones[]" rows="2" cols="40"></textarea><br><br>
    // `;

    grupo.innerHTML = `
        <hr>
        <label class="entrega-label">Tipo de Material:</label>
        <select name="material[]" required class="entrega-select"></select>

        <label class="entrega-label">Cantidad:</label>
        <input type="number" name="cantidad[]" min="1" required class="entrega-input">

        <label class="entrega-label">Condiciones de Entrega:</label>
        <textarea name="condiciones[]" rows="2" cols="40" class="entrega-input"></textarea>
    `;


    contenedor.appendChild(grupo);

    const selectMaterial = grupo.querySelector('select');
    cargarMateriales(puntoId, selectMaterial);
}