document.addEventListener('DOMContentLoaded', () => {
    // --- Modal Logic ---
    const modal = document.getElementById('result-modal');
    const modalMessage = document.getElementById('modal-message');
    const modalContent = modal.querySelector('.modal-content');
    const closeModalBtn = modal.querySelector('.modal-close-btn');

    function showModal(message, type) {
        modalMessage.innerHTML = message; // Use innerHTML to allow for formatting if needed
        modalContent.className = 'modal-content'; // Reset classes
        modalContent.classList.add(type); // 'success' or 'danger'
        modal.style.display = 'flex';
    }

    function hideModal() {
        modal.style.display = 'none';
    }

    closeModalBtn.addEventListener('click', hideModal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            hideModal();
        }
    });

    function downloadCSV(data, filename = 'predictions.csv') {
        if (!Array.isArray(data) || data.length === 0) {
            console.error('Invalid data for CSV conversion.');
            showModal('<strong>Ошибка:</strong> Не удалось сгенерировать CSV файл из-за неверного формата данных.', 'danger');
            return;
        }

        const csvRows = [];
        // Add header
        csvRows.push('id,predict');

        // Add data rows
        for (const row of data) {
            // Ensure both id and predict exist, otherwise skip row or use defaults
            if (row.id !== undefined && row.predict !== undefined) {
                csvRows.push(`${row.id},${row.predict}`);
            }
        }

        const csvString = csvRows.join('\n');
        const blob = new Blob([`\ufeff${csvString}`], { type: 'text/csv;charset=utf-8;' }); // Add BOM for Excel

        // Create a link and trigger the download
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    // --- Slider Value Display ---
    const sliders = document.querySelectorAll('input[type="range"]');
    sliders.forEach(slider => {
        const valueSpan = document.getElementById(`${slider.id}-value`);
        if (valueSpan) {
            slider.addEventListener('input', () => {
                valueSpan.textContent = slider.value;
            });
        }
    });

    // --- File Input Logic ---
    const fileInput = document.getElementById('file-input');
    const fileLabel = document.getElementById('file-label');
    const sendFileBtn = document.getElementById('send-file-btn');

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            const fileName = fileInput.files[0].name;
            fileLabel.textContent = `Файл: ${fileName}`;
            fileLabel.classList.add('file-loaded');
            sendFileBtn.disabled = false;
        } else {
            fileLabel.textContent = 'Выбрать файл';
            fileLabel.classList.remove('file-loaded');
            sendFileBtn.disabled = true;
        }
    });
    
    // --- Form Submission ---
    const form = document.getElementById('prediction-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const usernameInput = document.getElementById('username');
        const username = usernameInput.value.trim();
        if (!username) {
            alert('Пожалуйста, введите ваше имя.');
            usernameInput.focus();
            return;
        }

        const formData = new FormData(form);
        const data = {};
        for (const [key, value] of formData.entries()) {
            const input = form.querySelector(`[name="${key}"]`);
            if (input.type === 'checkbox') {
                data[key] = input.checked;
            } else {
                data[key] = value;
            }
        }
         // Manually add unchecked checkboxes as false
        form.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            if (!checkbox.checked) {
                data[checkbox.name] = false;
            }
        });


        try {
            const response = await fetch('/api/get_prediction/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                // For demonstration, if the API fails, mock a response
                if (response.status === 404) {
                    console.warn("API endpoint '/api/get_prediction/' not found. Using mocked data for demonstration.");
                    const mockPrediction = Math.random();
                    handlePrediction(mockPrediction, username);
                    return; 
                }
                throw new Error(`Ошибка сети: ${response.statusText}`);
            }

            const prediction = await response.json();
            handlePrediction(prediction.predict, username);

        } catch (error) {
            console.error('Ошибка при отправке формы:', error);
            showModal(`<strong>Произошла ошибка:</strong> ${error.message}. Попробуйте снова позже.`, 'danger');
        }
    });
    
    function handlePrediction(prediction, username) {
        const predictionNumber = parseFloat(prediction);
        let message;
        let type;

        if (predictionNumber > 50) {
            message = `<strong>${username}</strong>, пожалуйста, обратитесь к врачу. Вероятность проблем с сердцем <strong>${predictionNumber.toFixed(2)}%</strong>`;
            type = 'danger';
        } else {
            message = `<strong>${username}</strong>, вероятность проблем с сердцем <strong>${predictionNumber.toFixed(2)}%</strong>. Но если Вы зашли на этот сайт, вероятно есть предпосылки к болезням сердца. Рекомендуем обратится к врачу.`;
            type = 'success';
        }
        showModal(message, type);
    }

    sendFileBtn.addEventListener('click', async () => {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append('file', file);
            
            const originalButtonText = sendFileBtn.textContent;
            sendFileBtn.disabled = true;
            sendFileBtn.textContent = 'Отправка...';

            try {
                const response = await fetch('/api/get_predictions/', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const data = await response.json();
                    downloadCSV(data, `predictions_${file.name}.csv`);
                } else {
                    if (response.status === 404) {
                       console.warn("API endpoint '/api/get_predictions/' not found. Simulating download for demonstration.");
                       const mockData = [
                         { "id": "1", "predict": 85.2 },
                         { "id": "2", "predict": 12.4 }
                       ];
                       downloadCSV(mockData, `predictions_demo.csv`);
                       return;
                    }
                    throw new Error(`Ошибка сервера: ${response.statusText}`);
                }

            } catch(error) {
                console.error('Ошибка при отправке файла:', error);
                showModal(`<strong>Произошла ошибка при отправке файла:</strong> ${error.message}.`, 'danger');
            } finally {
                // Restore button state
                sendFileBtn.disabled = false;
                sendFileBtn.textContent = originalButtonText;
            }
        }
    });
});