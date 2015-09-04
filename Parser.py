import yaml
import json

#creating a model that maps to a mongo schema
def createMongoModel(model,schema):
    file=open('template//models//'+model[:-1]+".js","w")
    file.write("var mongoose     = require('mongoose');\n"+"var Schema= mongoose.Schema;\n")
    file.write("var "+model[:-1].title()+"Schema   = new Schema({\n")
    
    file.write(schema+"\n")
    file.write("});\n")
    file.write("module.exports = mongoose.model('"+model[:-1].title()+"', "+model[:-1].title()+"Schema);")
    file.close()
    
#creating a controller that maps to the model
def createMongoController(model,requests):
    api=[['/'+model]]     #add all the things required for the api.js
    schema=requests['schema'].split(" ")
    #print schema
    del requests['schema']
    file=open('template//controllers//'+model[:-1]+".js","w")
    file.write("var "+model[:-1].title()+" = require('../models/"+model[:-1]+"');\n\n")
    
    for i in requests:
        
        if(i=='post'):
            #handles post method to the main resource
            file.write("exports.save = function (req, res) {\n")
            file.write("var "+model[:-1]+"= new "+model[:-1].title()+"();\n")
            for j in schema:    #getting the parameters into the abov object
                param=j.rsplit(':')[0]
                file.write(model[:-1]+"."+param+"=req.body."+param+";\n")
            file.write(model[:-1]+".save(function(err) {\n")
            file.write("if (err) res.send(err);\nres.json({ message: 'created!' });\n});\n};\n\n")
            api[0].append('post:save')
        elif(i=='get'):
            #handles get  method to the main resource
            file.write("exports.see = function(req, res) {\n")
            file.write(model[:-1].title()+".find(function(err, val) {\n")
            file.write("if (err)\n\tres.send(err);\n\t\tres.json(val);\n}); \n};\n\n")
            api[0].append('get:see')
        
        else:
            #handles /song/songId get,post and etc.
            forapi=['/'+model+'/:'+i]
            #this is to append to api list at the end ['/songs/songId','get:ac']
            subrequests=requests[i]
            for sub in subrequests:
                #print sub
                if(sub=='get'):
                    file.write("exports.get"+i+" = function(req, res) {\n")
                    file.write("\t"+model[:-1].title()+".find({ '"+i+"':  req.params."+i+" }, function (err, rcd) {\n")
                    file.write("\t\tif (err) console.log(err);\n\t\tres.json(rcd);\n\t});\n};\n\n")
                    forapi.append('get:'+'get'+i)
                elif(sub=='post'):
                    continue
                elif(sub=='delete'):
                    file.write("exports.delete"+i+" = function (req, res) {\n")
                    file.write("\tvar query =" +model[:-1].title()+".remove({ '"+i+"':  req.params."+i+"});\n")
                    file.write( """\tif(query.exec()) res.json("'status':'1'");\n\telse res.json("'status':'0'"); \n};\n\n""")
                    forapi.append('delete:'+'delete'+i)
                elif(sub=='put'):
                    file.write("exports.update"+i+" = function (req, res) {\n")
                    file.write("\t"+model[:-1].title()+".update({ '"+i+"':  req.params."+i+"}, req.body , {} , function (err, count) {\n")
                    file.write("\t\tif (err) console.log(err);\n\t\tres.send({ 'updated': count });\n\t});\n};\n\n")
                    forapi.append('put:'+'update'+i)
            api.append(forapi)   
        
    file.close()
    return(api)

def addRoutes(controller,routes):
    #input to this function 'song',[['/songs', 'post:save', 'get:see']]
    f = open("template//routes//api.js", "a")
   
      
    #adding the link of controller to API
    f.write("var "+controller+"Controller = require('../controllers/"+controller+"');\n\n")
    
    for route in routes:
       
        count=0
        for i in route:
         
           
            if(count==0):
                f.write("router.route('"+i+"')\n")
            
            elif(i.rsplit(':')[0]=='get'):      #adding the get route to api of the given controller in list
                        f.write("\n\t.get("+controller+"Controller."+i.rsplit(':')[1]+")")
            
            elif(i.rsplit(':')[0]=='post'):
                        f.write("\n\t.post(function(req, res) {\n\t"+controller+"Controller."+i.rsplit(':')[1]+"(req, res)\n\t})")
            elif(i.rsplit(':')[0]=='delete'):
                        f.write("\n\t.delete(function(req, res) {\n\t"+controller+"Controller."+i.rsplit(':')[1]+"(req, res)\n\t})")
            elif(i.rsplit(':')[0]=='put'):
                        f.write("\n\t.put(function(req, res) {\n\t"+controller+"Controller."+i.rsplit(':')[1]+"(req, res)\n\t})")
                
            count+=1    
        f.write(";\n\n")
        
    f.close()

def addModuleExport():
    f = open("template//routes//api.js", "a")
    f.write("\n\nmodule.exports = router;")
    f.close()


    
#Loading the YAML into a dictionary.
yml = open("test.YAML","r")
data = yaml.load(yml)



baseUri=data['baseUri']
title=data['title']
version=data['version']
del data['baseUri']
del data['title']
del data['version']



for elements in data:
    
    createMongoModel(elements,data[elements]['schema'].replace(" ",","))
    routes=createMongoController(elements,data[elements])
    addRoutes(elements[:-1],routes)


addModuleExport()
