
// function post_name(obj){
//     var name = obj.innerHTML;
//     console.log(name);
//     $.post("select/",{"element_name":name},function(data){
//         // alert("Data: " + data + "\n" + "nStatus: " + status);
//         var obj1 = eval(data);
//         var tbody = $('#info');
//         $(obj1).each(function(index){
//             var val = obj1[index];
//             var tr=$("<tr></tr>");
//             tr.append("<td>" + (index + 1) + "</td>");
//             var str = val["lattice"]["a"] + "," + val["lattice"]["b"] + "," + val["lattice"]["c"] + "," + val["lattice"]["alpha"] + "," + val["lattice"]["beta"] + "," + val["lattice"]["gamma"]
//             tr.append("<td>" + str +"</td>");
//             tr.append("<td>" + 225 +"</td>");
//             tr.append("<td>" + "cubic" +"</td>");
//             tr.append("<td><a href = 'detail/'><span class='glyphicon glyphicon-chevron-right'></span></a></td>");
//             tbody.append(tr);
//         });
//         $('#info').replaceWith(tbody);
//     });
// }
var name1
var latticeparameters
function post_name(obj){
    var name = obj.innerHTML;
    name1 = name
    console.log(name);
    $.post("select/",{"element_name":name},function(data){
    // alert("Data: " + data + "\n" + "nStatus: " + status);
    var obj1 = eval(data);
    var tbody = $('#info');
    tbody[0].innerHTML="";
    $(obj1).each(function(index){
    var val = obj1[index];
    var tr=$("<tr></tr>");
    tr.append("<td>" + (index + 1) + "</td>");
    var str = val["lattice"]["a"] + "," + val["lattice"]["b"] + "," + val["lattice"]["c"] + "," + val["lattice"]["alpha"] + "," + val["lattice"]["beta"] + "," + val["lattice"]["gamma"]
    latticeparameters = str
    tr.append("<td>" + str +"</td>");
    tr.append("<td>" + 225 +"</td>");
    tr.append("<td>" + "cubic" +"</td>");
    // tr.append("<td><a href = ' "+obj1[0].sites[0].label+"&latticeparameters="+str+"'><span class='glyphicon glyphicon-chevron-right'></span></ a></td>");
    tr.append("<td><buttom onclick='post_info()'><span class='glyphicon glyphicon-chevron-right'></span></buttom></td>");
    tbody.append(tr);
    });
    $('#info').replaceWith(tbody);
    });
    
}

function post_info(){
    $.post("detail/", {"element_name":name1,"latticeparameters":latticeparameters},function(str_response){
        var obj = window.open("about:blank");   
        obj.document.write(str_response)
    });
}        
		