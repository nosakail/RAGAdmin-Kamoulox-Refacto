# RAGAdmin
Projet BUT3 : RAGAdmin, La Poste

La configuration des machines est la suivante :  

<table>
    <tr>
        <th>Machine</th>
        <th>Ip</th>
        <th>Port</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>Proxmox</td>
        <td>192.168.0.1</td>
        <td>8006</td>
        <td>Machine Proxmox qui accueille toutes les machines virtuelles / conteneurs virtuels.
    </tr>
    <tr>
        <td>Gitea</td>
        <td  rowspan="2">192.168.0.20</td>
        <td>3000</td>
        <td>Permet de versionner le code via un serveur git local.</td>
    </tr>
    <tr>
        <td>Jenkins</td>
        <td>8000</td>
        <td>Permet d'exécuter la chaine CI/CD</td>
    </tr>
    <tr>
        <td>Ubuntu</td>
        <td>192.168.0.21</td> <!-- Cellule fusionnée pour masquer la bordure -->
        <td>-</td>
        <td>Machine stockant le LLM</td>
    </tr>
    <tr>
        <td>-</td>
        <td>-</td> <!-- Cellule fusionnée pour masquer la bordure -->
        <td>-</td>
        <td>Machine permettant d'accéder à l'interface graphique du LLM.</td>
    </tr>
    <tr>
        <td>Chroma DB</td>
        <td>192.168.0.22</td> <!-- Cellule fusionnée pour masquer la bordure -->
        <td>8000</td>
        <td>Machine accueillant la base de données vectorielle du LLM.</td>
    </tr>
  
</table>

# Tous les tests
pytest tests/

# Un fichier spécifique
pytest tests/test_file_operations.py

# Avec couverture
pytest tests/ --cov=src/

