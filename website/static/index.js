function deleteNote(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId})
    }).then((_res) => {
        window.location.href = "/";
    });
}

function deleteCategory(categoryId){
    fetch('/delete-category', {
        method: 'POST',
        body: JSON.stringify({categoryId: categoryId})
    }).then((_res) => {
        window.location.href = "/add-category"
    })
}