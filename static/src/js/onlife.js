odoo.define('onlife.onlife', function (require) {
"use strict";

var screens = require('point_of_sale.screens');
var models = require('point_of_sale.models');
var gui = require('point_of_sale.gui');
var rpc = require('web.rpc');

models.load_fields('pos.config', 'invoice_journal_ids');

var _super_order = models.Order.prototype;    
models.Order = models.Order.extend({
    set_diario_id: function(id) {
        this.set({
            diario_id: id,
        });
    },
    get_diario_id: function() {
        return this.get('diario_id');
    },
    export_as_JSON: function() {
        var json = _super_order.export_as_JSON.apply(this,arguments);
        var diario_id = this.get('diario_id');
        if (diario_id) {
            json['invoice_journal_id'] = diario_id;
        }
        else {
            json['invoice_journal_id'] = this.pos.config.invoice_journal_id[0];
        }
        return json
    },
});

var JournalButton = screens.ActionButtonWidget.extend({
    template: 'JournalButton',

    button_click: function(){

    var self = this;
    self.select_journal();
    
    },
    select_journal: function(){
        var self = this;
        var filtro = [['id', 'in', this.pos.config.invoice_journal_ids]]
        rpc.query({
                model: 'pos.config',
                method: 'obtener_diarios',
                args: [[], filtro, []],
            })
            .then(function (diarios){
                var list = [];
                for (var i = 0; i < diarios.length; i++) {
                    var diario = diarios[i];
                    list.push({
                        'label': diario.name,
                        'item':  diario,
                    });
                }
                var gui = self.pos.gui;
                var orden = self.pos.get_order();
                gui.show_popup('selection', {
                    'title': 'Diario',
                    'list': list,
                    'confirm': function(line) {
                        orden.set_diario_id(line.id);
                    },
                });
            });
    },
});

screens.define_action_button({
    'name': 'journal_button',
    'widget': JournalButton,
});

});
