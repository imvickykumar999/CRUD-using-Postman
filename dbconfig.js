	
const config = {
    user: "sa",
    // port : parseInt(process.env.DB_PORT,1433),
    password: "MsSql1234",
    server: "LP38",
    database: "Data",
    options: {
      trustedconnection: true,
      enableArithAbort: true,
      trustServerCertificate: true,
      instancename: "",
    },
    // port: 1433;
    // port: 49693
  };
   
  module.exports = config;
  