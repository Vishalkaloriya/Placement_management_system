function fileValidation() 
{
    var fileInput = document.getElementById('resume');
    var filePath = fileInput.value;
    var allowedExtensions =
                            /(\.pdf)$/i;
    if (!allowedExtensions.exec(filePath)) 
    {
        alert('Invalid file type');
        fileInput.value = '';
        return false;
    }
}