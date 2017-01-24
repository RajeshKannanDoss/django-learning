var showErrorDiv = document.getElementById('alert-error');
var errorMessage = document.getElementById('error-message');
function showError(mes)
{
    showErrorDiv.style.display = 'block';
    errorMessage.innerHTML = mes;
    setTimeout(function(){
        showErrorDiv.style.display = 'none';
    }, 2500);
}

var showSuccessDiv = document.getElementById('alert-success');
var successMessage = document.getElementById('success-message');
function showSuccess(mes)
{
    showSuccessDiv.style.display = 'block';
    successMessage.innerHTML = mes;
    setTimeout(function(){
        showSuccessDiv.style.display = 'none';
    }, 2500);
}

export {showError}
export {showSuccess}
