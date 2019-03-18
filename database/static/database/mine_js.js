
function post_name(obj){
    var name = obj.innerHTML;
    console.log(name);
    $.post("select/",{"element_name":name},function(data){
        // alert("Data: " + data + "\n" + "nStatus: " + status);
        var obj1 = eval(data);
        var tbody = $('#info');
        $(obj1).each(function(index){
            var val = obj1[index];
            var tr=$("<tr></tr>");
            tr.append("<td>" + (index + 1) + "</td>");
            var str = val["lattice"]["a"] + "," + val["lattice"]["b"] + "," + val["lattice"]["c"] + "," + val["lattice"]["alpha"] + "," + val["lattice"]["beta"] + "," + val["lattice"]["gamma"]
            tr.append("<td>" + str +"</td>");
            tr.append("<td>" + 225 +"</td>");
            tr.append("<td>" + "cubic" +"</td>");
            tr.append("<td><a href = '#'><span class='glyphicon glyphicon-chevron-right'></span></a></td>");

            tbody.append(tr);
        });
        $('#info').replaceWith(tbody);
    });
}
		