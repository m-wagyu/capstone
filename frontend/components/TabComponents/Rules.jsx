import React, { useState, useEffect } from 'react';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import { Row, Col } from 'react-bootstrap'
import SuricataTableComponent from './components/SuricataTableComponent.jsx'
import ReloadButtonComponent from './components/ReloadButtonComponent.jsx'
import AddIcon from '@material-ui/icons/Add';

const test_data = [
    {
        "enable": "true",
        "sid": 929549,
        "gid": 150436,
        "protocol": "EST",
        "action": "TINCIDUNT",
        "message": "VENENATIS TRISTIQUE FUSCE"
    }, {
        "enable": "true",
        "sid": 191782,
        "gid": 43115,
        "protocol": "NONUMMY",
        "action": "CONDIMENTUM",
        "message": "IN IMPERDIET"
    }, {
        "enable": "true",
        "sid": 700432,
        "gid": 498456,
        "protocol": "ID",
        "action": "IN",
        "message": "TINCIDUNT LACUS"
    }, {
        "enable": "true",
        "sid": 655272,
        "gid": 940467,
        "protocol": "DOLOR",
        "action": "TINCIDUNT",
        "message": "ID MASSA"
    }, {
        "enable": "true",
        "sid": 902775,
        "gid": 745043,
        "protocol": "ELEIFEND",
        "action": "IN",
        "message": "IPSUM PRIMIS IN"
    }, {
        "enable": "true",
        "sid": 205231,
        "gid": 541014,
        "protocol": "MORBI",
        "action": "DUIS",
        "message": "AT VELIT EU"
    }, {
        "enable": "true",
        "sid": 911846,
        "gid": 687060,
        "protocol": "ULTRICES",
        "action": "SOLLICITUDIN",
        "message": "RUTRUM NEQUE AENEAN"
    }, {
        "enable": "true",
        "sid": 294230,
        "gid": 601784,
        "protocol": "NEQUE",
        "action": "QUISQUE",
        "message": "NON INTERDUM IN"
    }, {
        "enable": "true",
        "sid": 333604,
        "gid": 361241,
        "protocol": "NULLA",
        "action": "RHONCUS",
        "message": "MAGNA BIBENDUM IMPERDIET"
    }, {
        "enable": "true",
        "sid": 67303,
        "gid": 343474,
        "protocol": "SAGITTIS",
        "action": "POSUERE",
        "message": "HENDRERIT AT"
    }, {
        "enable": "true",
        "sid": 879454,
        "gid": 275159,
        "protocol": "LOBORTIS",
        "action": "MATTIS",
        "message": "NISI VENENATIS"
    }, {
        "enable": "true",
        "sid": 149708,
        "gid": 508050,
        "protocol": "PRAESENT",
        "action": "SOLLICITUDIN",
        "message": "EGET ELIT SODALES"
    }, {
        "enable": "true",
        "sid": 186197,
        "gid": 49854,
        "protocol": "PORTTITOR",
        "action": "ET",
        "message": "NON LECTUS"
    }, {
        "enable": "true",
        "sid": 45278,
        "gid": 867794,
        "protocol": "MAURIS",
        "action": "VESTIBULUM",
        "message": "NIBH QUISQUE"
    }, {
        "enable": "true",
        "sid": 508879,
        "gid": 89930,
        "protocol": "DICTUMST",
        "action": "EROS",
        "message": "FUSCE CONGUE DIAM"
    }, {
        "enable": "true",
        "sid": 366057,
        "gid": 414510,
        "protocol": "AENEAN",
        "action": "NEC",
        "message": "INTERDUM VENENATIS TURPIS"
    }, {
        "enable": "true",
        "sid": 352766,
        "gid": 326346,
        "protocol": "LAOREET",
        "action": "LUCTUS",
        "message": "PURUS PHASELLUS IN"
    }, {
        "enable": "true",
        "sid": 869427,
        "gid": 44068,
        "protocol": "MAECENAS",
        "action": "SED",
        "message": "JUSTO SIT AMET"
    }, {
        "enable": "true",
        "sid": 506011,
        "gid": 313216,
        "protocol": "AUCTOR",
        "action": "IN",
        "message": "TEMPUS SIT AMET"
    }, {
        "enable": "true",
        "sid": 482747,
        "gid": 147891,
        "protocol": "NISL",
        "action": "MORBI",
        "message": "ODIO ODIO ELEMENTUM"
    }, {
        "enable": "true",
        "sid": 198700,
        "gid": 971169,
        "protocol": "TEMPOR",
        "action": "JUSTO",
        "message": "IPSUM INTEGER A"
    }, {
        "enable": "true",
        "sid": 146497,
        "gid": 748381,
        "protocol": "IN",
        "action": "AUCTOR",
        "message": "IPSUM INTEGER A"
    }, {
        "enable": "true",
        "sid": 280154,
        "gid": 607983,
        "protocol": "VEL",
        "action": "VEL",
        "message": "NISL UT"
    }, {
        "enable": "true",
        "sid": 127347,
        "gid": 545715,
        "protocol": "FELIS",
        "action": "CONSEQUAT",
        "message": "CUBILIA CURAE MAURIS"
    }, {
        "enable": "true",
        "sid": 574101,
        "gid": 948173,
        "protocol": "AT",
        "action": "SED",
        "message": "NULLAM VARIUS NULLA"
    }, {
        "enable": "true",
        "sid": 58835,
        "gid": 678843,
        "protocol": "NON",
        "action": "IMPERDIET",
        "message": "HABITASSE PLATEA DICTUMST"
    }, {
        "enable": "true",
        "sid": 942430,
        "gid": 285849,
        "protocol": "RIDICULUS",
        "action": "TELLUS",
        "message": "MORBI VESTIBULUM"
    }, {
        "enable": "true",
        "sid": 764417,
        "gid": 142723,
        "protocol": "VOLUTPAT",
        "action": "LIGULA",
        "message": "DONEC UT DOLOR"
    }, {
        "enable": "true",
        "sid": 971656,
        "gid": 942996,
        "protocol": "EGET",
        "action": "ULTRICES",
        "message": "ELEMENTUM LIGULA VEHICULA"
    }, {
        "enable": "true",
        "sid": 224178,
        "gid": 557965,
        "protocol": "PRIMIS",
        "action": "SIT",
        "message": "VEHICULA CONDIMENTUM"
    }, {
        "enable": "true",
        "sid": 910635,
        "gid": 214444,
        "protocol": "VITAE",
        "action": "NON",
        "message": "QUAM NEC DUI"
    }, {
        "enable": "true",
        "sid": 425766,
        "gid": 613997,
        "protocol": "CRAS",
        "action": "NISL",
        "message": "CURAE NULLA"
    }, {
        "enable": "true",
        "sid": 608341,
        "gid": 367670,
        "protocol": "IN",
        "action": "VESTIBULUM",
        "message": "SED SAGITTIS NAM"
    }, {
        "enable": "true",
        "sid": 341828,
        "gid": 997182,
        "protocol": "FUSCE",
        "action": "ELEMENTUM",
        "message": "TEMPOR TURPIS"
    }, {
        "enable": "true",
        "sid": 121970,
        "gid": 129013,
        "protocol": "VENENATIS",
        "action": "LACINIA",
        "message": "FERMENTUM JUSTO NEC"
    }, {
        "enable": "true",
        "sid": 960719,
        "gid": 800358,
        "protocol": "VELIT",
        "action": "AT",
        "message": "ALIQUAM NON"
    }, {
        "enable": "true",
        "sid": 883090,
        "gid": 205286,
        "protocol": "TURPIS",
        "action": "RISUS",
        "message": "SIT AMET SAPIEN"
    }, {
        "enable": "true",
        "sid": 925594,
        "gid": 471016,
        "protocol": "QUIS",
        "action": "ELIT",
        "message": "SOCIIS NATOQUE"
    }, {
        "enable": "true",
        "sid": 140304,
        "gid": 636503,
        "protocol": "NULLAM",
        "action": "MAURIS",
        "message": "AENEAN AUCTOR GRAVIDA"
    }, {
        "enable": "true",
        "sid": 796117,
        "gid": 800056,
        "protocol": "TURPIS",
        "action": "AT",
        "message": "ANTE IPSUM PRIMIS"
    }, {
        "enable": "true",
        "sid": 243351,
        "gid": 717986,
        "protocol": "SAPIEN",
        "action": "AMET",
        "message": "ID LOBORTIS"
    }, {
        "enable": "true",
        "sid": 166631,
        "gid": 202537,
        "protocol": "NASCETUR",
        "action": "DAPIBUS",
        "message": "VOLUTPAT CONVALLIS MORBI"
    }, {
        "enable": "true",
        "sid": 915767,
        "gid": 817346,
        "protocol": "TEMPUS",
        "action": "IACULIS",
        "message": "CURABITUR GRAVIDA"
    }, {
        "enable": "true",
        "sid": 630277,
        "gid": 271141,
        "protocol": "NEC",
        "action": "ULTRICES",
        "message": "MATTIS ODIO DONEC"
    }, {
        "enable": "true",
        "sid": 753506,
        "gid": 506484,
        "protocol": "ENIM",
        "action": "SIT",
        "message": "LIBERO NULLAM SIT"
    }, {
        "enable": "true",
        "sid": 86450,
        "gid": 763402,
        "protocol": "NULLA",
        "action": "TURPIS",
        "message": "JUSTO ALIQUAM QUIS"
    }, {
        "enable": "true",
        "sid": 383690,
        "gid": 404563,
        "protocol": "ERAT",
        "action": "CONVALLIS",
        "message": "UT AT"
    }, {
        "enable": "true",
        "sid": 354370,
        "gid": 129943,
        "protocol": "TELLUS",
        "action": "QUAM",
        "message": "IACULIS DIAM"
    }, {
        "enable": "true",
        "sid": 72517,
        "gid": 21044,
        "protocol": "NUNC",
        "action": "ELEIFEND",
        "message": "INTERDUM IN ANTE"
    }, {
        "enable": "true",
        "sid": 799048,
        "gid": 441481,
        "protocol": "DONEC",
        "action": "AMET",
        "message": "NISI EU"
    }, {
        "enable": "true",
        "sid": 480751,
        "gid": 273743,
        "protocol": "AMET",
        "action": "VESTIBULUM",
        "message": "MASSA ID LOBORTIS"
    }, {
        "enable": "true",
        "sid": 622748,
        "gid": 382165,
        "protocol": "LOBORTIS",
        "action": "CUBILIA",
        "message": "SIT AMET JUSTO"
    }, {
        "enable": "true",
        "sid": 73000,
        "gid": 316046,
        "protocol": "ID",
        "action": "FAUCIBUS",
        "message": "LACUS AT"
    }, {
        "enable": "true",
        "sid": 979970,
        "gid": 749120,
        "protocol": "LUCTUS",
        "action": "CONSEQUAT",
        "message": "JUSTO ALIQUAM QUIS"
    }, {
        "enable": "true",
        "sid": 692159,
        "gid": 112410,
        "protocol": "INTERDUM",
        "action": "PRETIUM",
        "message": "HAC HABITASSE PLATEA"
    }, {
        "enable": "true",
        "sid": 35810,
        "gid": 916322,
        "protocol": "QUIS",
        "action": "ET",
        "message": "LIBERO NON MATTIS"
    }, {
        "enable": "true",
        "sid": 204870,
        "gid": 802277,
        "protocol": "NIBH",
        "action": "VITAE",
        "message": "ELEMENTUM IN"
    }, {
        "enable": "true",
        "sid": 294820,
        "gid": 298071,
        "protocol": "VEL",
        "action": "A",
        "message": "AT NUNC"
    }, {
        "enable": "true",
        "sid": 176191,
        "gid": 581149,
        "protocol": "EU",
        "action": "TURPIS",
        "message": "SEM DUIS"
    }, {
        "enable": "true",
        "sid": 816835,
        "gid": 14855,
        "protocol": "VOLUTPAT",
        "action": "ELEIFEND",
        "message": "ENIM BLANDIT MI"
    }, {
        "enable": "true",
        "sid": 168266,
        "gid": 804058,
        "protocol": "AMET",
        "action": "ANTE",
        "message": "SOLLICITUDIN MI"
    }, {
        "enable": "true",
        "sid": 57938,
        "gid": 563324,
        "protocol": "SEM",
        "action": "AT",
        "message": "DAPIBUS DOLOR"
    }, {
        "enable": "true",
        "sid": 342545,
        "gid": 480616,
        "protocol": "ID",
        "action": "ID",
        "message": "PHASELLUS SIT AMET"
    }, {
        "enable": "true",
        "sid": 447428,
        "gid": 809565,
        "protocol": "SED",
        "action": "AUGUE",
        "message": "TRISTIQUE EST"
    }, {
        "enable": "true",
        "sid": 202845,
        "gid": 10233,
        "protocol": "MORBI",
        "action": "ELIT",
        "message": "METUS AENEAN"
    }, {
        "enable": "true",
        "sid": 438482,
        "gid": 533337,
        "protocol": "NULLA",
        "action": "AUGUE",
        "message": "UT VOLUTPAT SAPIEN"
    }, {
        "enable": "true",
        "sid": 842431,
        "gid": 219866,
        "protocol": "VOLUTPAT",
        "action": "IN",
        "message": "CONVALLIS MORBI"
    }, {
        "enable": "true",
        "sid": 692587,
        "gid": 114843,
        "protocol": "ET",
        "action": "MAURIS",
        "message": "SAPIEN NON MI"
    }, {
        "enable": "true",
        "sid": 676048,
        "gid": 845030,
        "protocol": "A",
        "action": "MAURIS",
        "message": "CONSEQUAT UT NULLA"
    }, {
        "enable": "true",
        "sid": 539232,
        "gid": 516836,
        "protocol": "SEMPER",
        "action": "AENEAN",
        "message": "QUIS LECTUS SUSPENDISSE"
    }, {
        "enable": "true",
        "sid": 870196,
        "gid": 812584,
        "protocol": "DUIS",
        "action": "IMPERDIET",
        "message": "SOLLICITUDIN VITAE"
    }, {
        "enable": "true",
        "sid": 776301,
        "gid": 107603,
        "protocol": "PRAESENT",
        "action": "QUIS",
        "message": "PURUS EU MAGNA"
    }, {
        "enable": "true",
        "sid": 290156,
        "gid": 47332,
        "protocol": "RUTRUM",
        "action": "IN",
        "message": "EU EST"
    }, {
        "enable": "true",
        "sid": 401259,
        "gid": 689057,
        "protocol": "PARTURIENT",
        "action": "CONGUE",
        "message": "SAPIEN VARIUS UT"
    }, {
        "enable": "true",
        "sid": 784638,
        "gid": 13290,
        "protocol": "LECTUS",
        "action": "SED",
        "message": "AMET ELEIFEND PEDE"
    }, {
        "enable": "true",
        "sid": 372299,
        "gid": 100814,
        "protocol": "MAURIS",
        "action": "DICTUMST",
        "message": "EGET EROS"
    }, {
        "enable": "true",
        "sid": 611000,
        "gid": 479203,
        "protocol": "AC",
        "action": "IN",
        "message": "AUCTOR SED TRISTIQUE"
    }, {
        "enable": "true",
        "sid": 127077,
        "gid": 653672,
        "protocol": "CUBILIA",
        "action": "VESTIBULUM",
        "message": "CUBILIA CURAE DUIS"
    }, {
        "enable": "true",
        "sid": 320199,
        "gid": 843978,
        "protocol": "MAURIS",
        "action": "INTERDUM",
        "message": "VESTIBULUM VELIT"
    }, {
        "enable": "true",
        "sid": 961853,
        "gid": 603435,
        "protocol": "EGESTAS",
        "action": "ET",
        "message": "EU SAPIEN"
    }, {
        "enable": "true",
        "sid": 865508,
        "gid": 986835,
        "protocol": "NULLAM",
        "action": "SAPIEN",
        "message": "PURUS EU MAGNA"
    }, {
        "enable": "true",
        "sid": 342121,
        "gid": 817012,
        "protocol": "SIT",
        "action": "A",
        "message": "VOLUTPAT IN CONGUE"
    }, {
        "enable": "true",
        "sid": 565207,
        "gid": 528548,
        "protocol": "ID",
        "action": "CONGUE",
        "message": "NULLA MOLLIS"
    }, {
        "enable": "true",
        "sid": 418407,
        "gid": 719258,
        "protocol": "PELLENTESQUE",
        "action": "VESTIBULUM",
        "message": "EROS VESTIBULUM"
    }, {
        "enable": "true",
        "sid": 490152,
        "gid": 893740,
        "protocol": "ETIAM",
        "action": "FUSCE",
        "message": "ACCUMSAN ODIO CURABITUR"
    }, {
        "enable": "true",
        "sid": 521037,
        "gid": 553471,
        "protocol": "ANTE",
        "action": "MAURIS",
        "message": "ANTE IPSUM PRIMIS"
    }, {
        "enable": "true",
        "sid": 340530,
        "gid": 514233,
        "protocol": "CRAS",
        "action": "PRETIUM",
        "message": "DONEC UT"
    }, {
        "enable": "true",
        "sid": 298466,
        "gid": 49390,
        "protocol": "PORTTITOR",
        "action": "HAC",
        "message": "NON VELIT"
    }, {
        "enable": "true",
        "sid": 354515,
        "gid": 658171,
        "protocol": "VESTIBULUM",
        "action": "ID",
        "message": "VESTIBULUM SAGITTIS SAPIEN"
    }, {
        "enable": "true",
        "sid": 143800,
        "gid": 649026,
        "protocol": "EU",
        "action": "CONSECTETUER",
        "message": "TORTOR ID NULLA"
    }, {
        "enable": "true",
        "sid": 654286,
        "gid": 409984,
        "protocol": "COMMODO",
        "action": "VESTIBULUM",
        "message": "QUIS LECTUS"
    }, {
        "enable": "true",
        "sid": 893059,
        "gid": 909565,
        "protocol": "MORBI",
        "action": "POSUERE",
        "message": "ALIQUET MAECENAS LEO"
    }, {
        "enable": "true",
        "sid": 75304,
        "gid": 472900,
        "protocol": "DOLOR",
        "action": "SEM",
        "message": "MI SIT"
    }, {
        "enable": "true",
        "sid": 349732,
        "gid": 120029,
        "protocol": "CUBILIA",
        "action": "SEM",
        "message": "TELLUS NULLA UT"
    }, {
        "enable": "true",
        "sid": 748878,
        "gid": 322768,
        "protocol": "DOLOR",
        "action": "LECTUS",
        "message": "NON LIGULA PELLENTESQUE"
    }, {
        "enable": "true",
        "sid": 271984,
        "gid": 113963,
        "protocol": "IMPERDIET",
        "action": "DIAM",
        "message": "VOLUTPAT ERAT"
    }, {
        "enable": "true",
        "sid": 314756,
        "gid": 558215,
        "protocol": "EST",
        "action": "DONEC",
        "message": "AMET CONSECTETUER ADIPISCING"
    }, {
        "enable": "true",
        "sid": 271201,
        "gid": 432899,
        "protocol": "AC",
        "action": "ET",
        "message": "PELLENTESQUE ULTRICES PHASELLUS"
    }, {
        "enable": "true",
        "sid": 798909,
        "gid": 70454,
        "protocol": "NEQUE",
        "action": "NULLA",
        "message": "DONEC QUIS"
    }, {
        "enable": "true",
        "sid": 302947,
        "gid": 570820,
        "protocol": "AMET",
        "action": "VOLUTPAT",
        "message": "NEQUE VESTIBULUM EGET"
    }
]

const columns = [
    {
        title: "Enable",
        data_row_name: "enable",
        title_props: { align: "center" }, data_row_props: { component: "th", scope: "row", align: "center" }
    },
    {
        title: "SID",
        data_row_name: "sid",
        title_props: { align: "center" }, data_row_props: { align: "center" }
    },
    {
        title: "GID",
        data_row_name: "gid",
        title_props: { align: "center" }, data_row_props: { align: "center" }
    },
    {
        title: "Protocol",
        data_row_name: "protocol",
        title_props: { align: "center" }, data_row_props: { align: "center" }
    },
    {
        title: "Action",
        data_row_name: "action",
        title_props: { align: "center" }, data_row_props: { align: "center" }
    },
    {
        title: "Message",
        data_row_name: "message",
        title_props: { align: "center" }, data_row_props: { align: "center" }
    },
]

export default function Rules() {

    const [rules, setRules] = useState(test_data)

    function getRules() {
        console.log("refresh rules");
    }

    function addNewRules() {
        console.log("add new rules")
    }

    return (
        <>
            <Row className="w-100 p-0 m-0">
                <Col className="p-0"><Typography variant="h5">Network Rules</Typography></Col>
                <Col className="p-0 d-flex justify-content-end">
                    <Button variant="contained" color="secondary" disableElevation startIcon={<AddIcon />} className="mr-3" onClick={addNewRules}>Add Rules</Button>
                    <ReloadButtonComponent reloadDataFunc={getRules} />
                </Col>
            </Row>
            <br />

            <SuricataTableComponent columns={columns} data={rules} />

        </>
    )
}