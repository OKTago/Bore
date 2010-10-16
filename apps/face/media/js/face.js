dojo.addOnLoad(function() {
    dojo.require("dojo.parser");
    dojo.require("dijit.form.Button");
    
    dojo.addOnLoad(function() {
        dojo.parser.parse();
    });
});

Face = {
    removeExfriend: function(id, butt) {
        dojo.xhrPost({
            url: "delete/"+id+"/",
            method: "POST",
            handleAs: "text",
            load: function(response) {
                dnode = butt.parentNode;
                anim = dojo.fadeOut({node:dnode});
                var killdiv = function() { dojo.destroy(dnode); }
                anim.onEnd = killdiv;
                anim.play();
            }
        });
    }
}
