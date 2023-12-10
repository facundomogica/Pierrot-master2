function traeRecetas() {
    const apiKey = '1';
    let contenido = document.getElementById('contenido');
  
    fetch('https://www.themealdb.com/api/json/v1/1/random.php')
      .then(response => response.json())
      .then(data => {
        const receta = data.meals[0];
        contenido.innerHTML = `
          <h2 class= titulo >${receta.strMeal}</h2>
            
          <img  class="foto" src="${receta.strMealThumb}" alt="${receta.strMeal}">
          <p class= "instrucciones">${receta.strInstructions}</p>
          
        `;
      })
      .catch(error => console.error('Error al obtener la receta:', error));
  }
  