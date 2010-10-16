dojo.addOnLoad(function() {
    dojo.require("dojo.parser");
    dojo.require("dijit.form.Button");
    
    dojo.addOnLoad(function() {
        dojo.parser.parse();
    });
});

Face = {
    removeExfriend: function(id) {
        console.log(id);
    }
}
