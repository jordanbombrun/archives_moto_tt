## Pour installation sur linux 

### sources et environnement
git clone https://github.com/jordanbombrun/archives_moto_tt.git

git checkout front_flask

cd archives_moto_tt

chmod +x setup.sh 

./setup.sh

### BDD : init schema et data
app/database/init_db.py