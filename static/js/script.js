

let btn=document.querySelector('#modier')

let inputId=document.querySelectorAll('#numero')
let inputusername=document.querySelectorAll('#username')
let inputemail=document.querySelectorAll('#email')

inputId.forEach(function(item){
    item.setAttribute("disabled", "")
    item.classList.add('input')
})

inputusername.forEach(function(item){
    item.setAttribute("disabled", "")
    item.classList.add('input')
})

inputemail.forEach(function(item){
    item.setAttribute("disabled", "")
    item.classList.add('input')
})


btn.addEventListener('click', function(e){
    e.stopPropagation()
    e.preventDefault()
        
    document.querySelector('#numero').removeAttribute("disabled")
    document.querySelectorAll('#numero').classList.remove('input')
   
    
   
    item.removeAttribute("disabled")
    item.classList.remove('input')
   
    
    
    item.removeAttribute("disabled")
    item.classList.remove('input')
    
  
})

// btn.addEventListener('click', function(){

// })
