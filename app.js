const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

let datums_drank1=[]
let aantaldranken_drank1=[]
let datums_drank2=[]
let aantaldranken_drank2=[]
let datums_drank3=[]
let aantaldranken_drank3=[]
let chart=''

let myChart = document.getElementById('myChart').getContext('2d')
const listenToUI = function(){
  const btn_passoa= document.querySelector('.btn_passoa')
  const btn_pisang= document.querySelector('.btn_pisang')
  const btn_safari= document.querySelector('.btn_safari')
  const btn_reiniging=document.querySelector('.btn_spoeling')
  const btn_pssoa= document.querySelector('.Passoa')
  
  if(btn_pssoa){
    btn_pssoa.addEventListener('click',function(){

    }
    
    )
  }

  if(btn_reiniging){
    btn_reiniging.addEventListener('click',function(){
      console.log('REINING')
      socket.emit("F2B_spoeling")
    })
  }

  if(btn_passoa){
    btn_passoa.addEventListener('click',function(){
      console.log('passoa')
      socket.emit("F2B_passoa")
    })
  }

  if(btn_pisang){
    btn_pisang.addEventListener('click',function(){
      console.log('pisang')
      socket.emit("F2B_pisang")
    })
  }
  if(btn_safari){
    btn_safari.addEventListener('click',function(){
      console.log('safari')
      socket.emit("F2B_safari")
    })
  }

}

const listenToSocket = function () {
    socket.on("connected", function () {
      console.log("verbonden met socket webserver");
    });
    socket.on("B2F_status_update",function(json){
        console.log('verbonden')
        console.log(json)
        
        for(const i of json.Safari){
          datums_drank1.push(i.Datum)
          aantaldranken_drank1.push(i.AantalDranken)
        }

        for(const i of json.Pisang){
          datums_drank2.push(i.Datum)
          aantaldranken_drank2.push(i.AantalDranken)
        }

        for(const i of json.Passoa){
          datums_drank3.push(i.Datum)
          aantaldranken_drank3.push(i.AantalDranken)
        }

        
      
        listenToChart(datums_drank1,aantaldranken_drank1,datums_drank2,aantaldranken_drank2,datums_drank3,aantaldranken_drank3)
    })
}

const listenToChart = function(json){


  let chart = new Chart(myChart,{
    type:'bar',
    data:{
      labels:datums_drank1,
      datasets:[{ label:'Aantal Dranken',data:aantaldranken_drank1
    }]
  }
    ,
    options:{
      scales:{
        yAxes:[{
          ticks:{
            beginAtZero:true
          }
        }]
      }
    }
  })




  if(document.querySelector('.Passoa')){
    chart.data.datasets[0].data=aantaldranken_drank3
    chart.data.labels=datums_drank3
    
    chart.update()

  }  

  if(document.querySelector('.Safari')){
    chart.data.datasets[0].data=aantaldranken_drank1
    chart.data.labels=datums_drank1
    
    chart.update()

  }

  if(document.querySelector('.Pisang')){
    chart.data.datasets[0].data=aantaldranken_drank2
    chart.data.labels=datums_drank2
    
    chart.update()

  }


}


document.addEventListener("DOMContentLoaded", function () {
    console.info("DOM geladen");
    listenToSocket();
    listenToChart();
    listenToUI();
  });