<div class="clearfix" style="padding: 0px; padding-left: 100px; display: flex; flex-wrap: nowrap; justify-content: space-evenly; align-items:center">
<a href="http://bimcv.cipf.es/"><img src="https://github.com/BIMCV-CSUSP/DiSMed/blob/master/images/logoinst.png?raw=true"</a><a href="http://ceib.san.gva.es"></a><a href="https://deephealth-project.eu/"><img src="https://github.com/BIMCV-CSUSP/DiSMed/blob/master/images/DEEPHEALTH.png" width="200px" class="center-block" style=" display: inline-block;"></a></div>
<br></br>

# DiSMed - De-identifying Spanish Medical texts

## Databases

This folder contains the six database files used to randomize the tagged Named Entities. 

### address.csv

This file contains a database about all local council addresses from Spain, retrieved from the [Open Data Initiative of the Government of Spain](https://datos.gob.es/en/peticiones-datos/direcciones-tel-y-cif-de-todos-los-ayuntamientos-de-espana). Its contents are distributed in 6 columns:

| n_mun   | dir_tipo_via | Dir_Via        | dir_cp | n_mun   | N_PROV  |
|---------|--------------|----------------|--------|---------|---------|
| Ababuj  | C/           | "Iglesia, 8"   | 44155  | Ababuj  | TERUEL  |
| ...     | ...          | ...            | ...    | ...     | ...     |
| Zurgena | Calle        | "del Mesón, 1" | 4650   | Zurgena | ALMERÍA |

* **n_mun**: Municipality name
* **dir_tipo**: Street type
* **Dir_Via**: Road name
* **dir_cp**: Zip code
* **n_mun**: Municipality name
* **N_PROV**: Province name

### PoblacionMunicipios.csv

This file contains a database of all municipalities in Spain, retrieved from [National Statistics Institute](https://www.ine.es/dynt3/inebase/es/index.htm?padre=517&capsel=525). Its contents are distributed in two columns:

| NOMBRE    | POB19 |
|-----------|-------|
| Abengibre | 790   |
| ...       | ...   |
| Zuera     | 8565  |

* **NOMBRE**: Municipality name
* **POB19**: Number of population of that municipality


### CentrosSalud.csv

This file contains a database about all outpatients clinics in Spain, retrieved from the [National Outpatients Clinics Index from Ministerio de Sanidad, Consumo y Bienestar Social](https://www.mscbs.gob.es/ciudadanos/prestaciones/centrosServiciosSNS/centrosSalud/home.htm).  Its contents are distributed in 7 columns, including an index:

|       | PROVINCIAS | MUNICIPIO       | TIPOCENTRO        | NOMBRE          | DIRECCION              | CP    |
|-------|------------|-----------------|-------------------|-----------------|------------------------|-------|
| 0     | ALMERÍA    | Almería         | CENTRO SALUD      | ALMERÍA CENTRO  | "C/ SAN LEONARDO, Nº7" | 4002  |
| ...   | ...        | ...             | ...               | ...             | ...                    | ...   |
| 13130 | ZARAGOZA   | Pozuel de Ariza | CONSULTORIO LOCAL | POZUEL DE ARIZA | "CL MAYOR, Nº 33"      | 42269 |

* **PROVINCIAS**: Province name
* **MUNICIPIO**: Municipality name
* **TIPOCENTRO**: Clinic type
* **NOMBRE**: Clinic name
* **DIRECCION**: Clinic address
* **CP**: Zip code

### hospitals.csv

This file contains a database about all hospitals in Spain, retrieved from the [National Hospital Index from Ministerio de Sanidad, Consumo y Bienestar social](https://www.mscbs.gob.es/ciudadanos/prestaciones/centrosServiciosSNS/hospitales/home.htm). Its contents are distributed in 5 columns:

| NOMBRE                          | DIRECCION             | MUNICIPIOS      | PROVINCIAS | CODPOSTAL |
|---------------------------------|-----------------------|-----------------|------------|-----------|
| HOSPITAL UNIVERSITARIO DE ARABA | "JOSÉ ATXOTEGUI, S/N" | Vitoria-Gasteiz | ÁLAVA      | 1009      |
| ...                             | ...                   | ...             | ...        | ...       |
| HOSPITAL COMARCAL               | "CTRA. REMONTA, 2"    | Melilla         | MELILLA    | 52005     |

* **NOMBRE**: Hospital name
* **DIRECCION**: Hospital address
* **MUNICIPIOS**: Municipality name
* **PROVINCIAS**: Province name
* **CODPOSTAL**: Zip code

### names.csv

This file contains a database of all names in Spain with a frecuency equal or greater to 20, retrieved from the [National Statistics Institute](https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177009&menu=ultiDatos&idp=1254734710990). Its contents are distributed in 2 columns:

| Nombre  | Frecuencia |
|---------|------------|
| ANTONIO | 678425     |
| ...     | ...        |
| ZARUHI  | 20         |

* **Nombre**: Name
* **Frecuencia**: Number of people registered with that name

### surnames.csv

This file contains a database of all surnames in Spain with a frecuency equal or greater to 20, retrieved from the [National Statistics Institute](https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177009&menu=ultiDatos&idp=1254734710990). Its contents are distributed in 2 columns:

| Nombre  | Frecuencia |
|---------|------------|
| GARCIA  | 1464633    |
| ...     | ...        |
| ZUDOR   | 20         |

* **Nombre**: Surname
* **Frecuencia**: Number of people registered with that surname