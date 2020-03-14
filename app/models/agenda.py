from index import db, ma

#creating the agenda table
class AgendaModel(db.Model):
    __tablename = 'agendas'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    agenda = db.Column(db.String(), nullable = False)



    #Creating the agenda records
    def createRecord(self):
        db.session.add(self)
        db.session.commit()
        return self

    #fetch all agendas
    @classmethod
    def fetchAgendas(cls):
        agendas = cls.query.all()
        return agendas
    
    #fetch agendas by id
    @classmethod
    def fetch_agendas_by_id(cls, id):
        agendas = cls.query.filter_by(id = id).first()
        return agendas





# schemas which allow us to regulate or melimit the data we want to expose to the consumer
class AgendaSchema(ma.Schema):
    class Meta:
        #fields to expose
        fields = ('id', 'title', 'agenda')
