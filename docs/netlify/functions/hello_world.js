exports.handler=async function(e,n){return{statusCode:200,body:JSON.stringify({message:"Hello World!",event:e,context:n,proc_env:process.env})}};