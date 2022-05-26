window.onload = function()
{
    fetch('http://localhost:3000/drivers')
    .then(res => res.json()).then((drivers) => 
    {
        console.log(drivers);
        var table = document.getElementById('myTable')
        for (var i = 0; i < drivers.length ; i++) {
            var row = `<tr> 
                            <td>${drivers[i]._id}</td>
                            <td>${drivers[i].license}</td>
                            <td>${drivers[i].lastName}</td>
                            <td>${drivers[i].firstName}</td>
                            <td>${drivers[i].contact}</td>         
                    </tr>`
            table.innerHTML += row     
        }        
    });   
};
