// get all the stars
const one = document.getElementById('first_star')
const two = document.getElementById('second_star')
const three = document.getElementById('third_star')
const four = document.getElementById('fourth_star')
const five = document.getElementById('fifth_star')
// get the form, confirm-box and csrf token
const form = document.querySelector('.priv_rating_form')
const msg = document.getElementById('msg-area')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

// Change classes of stars based on hover
const handleHoveringDisplay=(star_num_int)=>{
    const stars = form.children
    console.log(stars[0])
    for (let i=0; i < stars.length; i++) {
        if(i <= star_num_int) {
            stars[i].classList.add('checked')
        } else {
            stars[i].classList.remove('checked')
        }
    }
}

// Change star apparence based on hover 
const handleHovering=(star_id)=>{
    switch(star_id){
        case 'first_star':{
            handleHoveringDisplay(1)
            return
        }
        case 'second_star':{
            handleHoveringDisplay(2)
            return
        }
        case 'third_star':{
            handleHoveringDisplay(3)
            return
        }
        case 'fourth_star':{
            handleHoveringDisplay(4)
            return
        }
        case 'fifth_star':{
            handleHoveringDisplay(5)
            return
        }
        default:{
            handleHoveringDisplay(0)
        }
    }
}

// Translates string id to corresponding rating
const getRatingFromId =(star_id)=>{
    switch(star_id){
        case 'first_star':{
            return 1
        }
        case 'second_star':{
            return 2
        }
        case 'third_star':{         
            return 3
        }
        case 'fourth_star':{           
            return 4
        }
        case 'fifth_star':{
            return 5
        }
        default:{
            return 0
        }
    }
}

if (one) {
    const arr = [one, two, three, four, five]
    // Add hover and click event listners to all stars
    arr.forEach(item=> item.addEventListener('mouseover', (event)=>{
        handleHovering(event.target.id)
    }))

    arr.forEach(item=> item.addEventListener('click', (event)=>{
        const star_id = event.target.id
        
        let submitted = false
        // When a star is clicked
        form.addEventListener('submit', elem=>{
            elem.preventDefault()
            if (submitted) {
                return
            }
            submitted = true
            // Get recipe id
            const recipe_id = elem.target.id
            // value of the rating translated into numeric
            const val_num = getRatingFromId(star_id)
            // Run the rating view with ajax
            $.ajax({
                type: 'POST',
                url: '/rate/',
                data: {
                    'csrfmiddlewaretoken': csrf[0].value,
                    'recipe_id': recipe_id,
                    'rating': val_num,
                },
                success: function(response){
                    if(response.success == 'true' || response.success =='already_rated'){
                        window.location.assign(response.url)
                    }
                    else{
                        msg.innerHTML = `<h3> ${response.errmsg}</h3>`
                        form.classList.add('hidden')
                    }
                },
                error: function(error){
                    console.log(error)
                    msg.innerHTML = `<h3> An error occurred!</h3>`
                }
            })
        })
    }))
}