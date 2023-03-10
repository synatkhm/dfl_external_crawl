function OnLoad() {

}

function OnChangeCity() {
    var city_name = document.getElementById("city_name").value;
    var str_city_list = document.getElementById("str_city_list").value;
    var str_area_list = document.getElementById("str_area_list").value;

    var city_list = JSON.parse(str_city_list.replace(/\'/g, '"'));
    var area_list = JSON.parse(str_area_list.replace(/\'/g, '"'));

    city_id = city_list.filter(function (entry) {
        return entry.name === city_name;
    })[0]['city_id'];

    choose_area_name = area_list.filter(
        function (entry) {
            return entry.city_id === city_id;
        }
    )

    areas_name = document.getElementById("areas_name");
    while (areas_name.options.length > 0) {
        areas_name.remove(0);
    }

    var objOption = document.createElement("option");
    objOption.text = "Choose area"
    objOption.value = "Choose area"
    areas_name.options.add(objOption);
    for (let i = 0; i < choose_area_name.length; i++) {
        var objOption = document.createElement("option");
        objOption.text = choose_area_name[i]['name']
        objOption.value = choose_area_name[i]['id']
        areas_name.options.add(objOption);
    }

}

function onClickCrawlNewAid() {
    sendMessage('', true);
    var selected_area = document.getElementById('areas_name');
    if (selected_area.value == 'Choose area') {
        sendMessage('Message: Please choose area.');
    } else {
        sendMessage('Crawl new aid is in progress...', true)
        requestCrawlNewAid(selected_area.value);
    }

}

function onClickCrawlNewAidLog() {
    sendMessage('');
    var selected_area = document.getElementById('areas_name');
    if (selected_area.value == 'Choose area') {
        sendMessage('Message: Please choose area.');
    } else {
        var area_id = selected_area.value;
        window.open(window.location.href + 'crawl-new-aid/logs/' + area_id, '_blank');
    }
}

function uploadData(){
    sendMessage('');
    var selected_area = document.getElementById('areas_name');
    if (selected_area.value == 'Choose area') {
        sendMessage('Message: Please choose area.');
    } else {
        var area_id = selected_area.value;
        sendMessage('Upload data is in progress...', true)
        try {
            var url = window.location.href + "upload-crawl-new-aid/" + area_id;
            axios.post(url)
                .then(function (response) {
                    if (response.status == 200) {
                        if (response.data['status'] == true) {
                            sendMessage(response.data['message'], true);
                        }else{
                            sendMessage(response.data['message']);
                        }
                    }else{
                        sendMessage('Upload data fail.');
                    }
                   
                })
        } catch (e) {
            sendMessage('Upload data fail.');
            console.log(e.message)
        }
    }
}



function sendMessage(txt, is_success=false) {
    document.getElementById('label_message_primary').innerText='';
    document.getElementById('label_message').innerText =''; 
    if(is_success){
        document.getElementById('label_message_primary').innerText = txt;
    }else{
        document.getElementById('label_message').innerText = txt;
    }
    
}


function add_data_into_table(jsonData) {

    var data = [];
    // Loop through the JSON data and create table rows
    jsonData.forEach((item) => {

        // Get the values of the current object in the JSON data
        let vals = Object.values(item);
        var data_row = [];
        // Loop through the values and create table cells
        var i = 0;
        vals.forEach((elem) => {
            if (i == 9 || i == 2) {
                if (elem != '') {
                    data_row.push(elem.toString().slice(0, 30) + '...');
                } else {
                    data_row.push('');
                }

            } else {
                data_row.push(elem);
            }
            i++;
        });
        data.push(data_row);
    });
    var table = $('#dataTable').DataTable();
    table.clear().draw();
    table.rows.add(data).draw();
}

async function getData() {
    var selected_area = document.getElementById('areas_name');
    var area_id = selected_area.value;
    if (area_id != "Choose area") {
        try {
            var url = window.location.href + "crawl-new-aid/" + area_id;
            axios.post(url)
                .then(function (response) {
                    if (response.status == 200) {
                        if (response.data != "") {
                            var data = JSON.parse(response.data);
                            add_data_into_table(data);
                            return
                            //var table = $('#dataTable');

                        }
                    }
                    add_data_into_table([]);
                })
        } catch (e) {
            console.log(e.message)
            // stop();
        }
    }
}


function onClickRefresh(){
    getData();
}

function requestCrawlNewAid(area_id) {
    var url = window.location.href + 'crawl-new-aid';
    axios.post(url,{ "area_id": area_id } 
      )
                .then(function (response) {
                    sendMessage(response.data['message'], true)
                    getData();
                })
    window.open(window.location.href + 'crawl-new-aid/logs/' + area_id, '_blank');
}

function logOut(){
    console.log();
    axios.post(window.location.origin+'/logout')
                .then(function (response) {
                    window.location.href=window.location.origin+'/login'
                })
}
