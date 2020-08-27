import React, { useState, useEffect } from 'react';
import Typography from '@material-ui/core/Typography';
import { Row, Col } from 'react-bootstrap'

import SuricataTableComponent from './components/SuricataTableComponent.jsx'
import ReloadButtonComponent from './components/ReloadButtonComponent.jsx'

const test_data = [{
    "time": "02/13/2020",
    "type": "MASSA",
    "message": "LOREM INTEGER TINCIDUNT ANTE VEL"
}, {
    "time": "08/12/2015",
    "type": "DUIS",
    "message": "PURUS SIT AMET"
}, {
    "time": "08/22/2015",
    "type": "NEQUE",
    "message": "VEL AUGUE VESTIBULUM ANTE IPSUM"
}, {
    "time": "09/21/2019",
    "type": "SAPIEN",
    "message": "PULVINAR LOBORTIS EST PHASELLUS SIT AMET"
}, {
    "time": "09/08/2011",
    "type": "NULLA",
    "message": "QUIS ORCI NULLAM MOLESTIE NIBH"
}, {
    "time": "01/22/2018",
    "type": "QUISQUE",
    "message": "DIS PARTURIENT MONTES NASCETUR RIDICULUS MUS VIVAMUS"
}, {
    "time": "03/07/2020",
    "type": "QUIS",
    "message": "EU INTERDUM EU TINCIDUNT IN"
}, {
    "time": "10/05/2017",
    "type": "NIBH",
    "message": "VESTIBULUM SAGITTIS SAPIEN"
}, {
    "time": "04/28/2011",
    "type": "JUSTO",
    "message": "ALIQUET AT FEUGIAT NON PRETIUM"
}, {
    "time": "09/05/2016",
    "type": "CURAE",
    "message": "EGET ORCI VEHICULA CONDIMENTUM CURABITUR IN"
}, {
    "time": "04/25/2020",
    "type": "IN",
    "message": "LACINIA EGET TINCIDUNT EGET TEMPUS"
}, {
    "time": "05/11/2019",
    "type": "INTERDUM",
    "message": "NON MATTIS PULVINAR NULLA PEDE ULLAMCORPER AUGUE"
}, {
    "time": "12/28/2010",
    "type": "CURABITUR",
    "message": "NULLA NISL NUNC NISL DUIS BIBENDUM FELIS"
}, {
    "time": "03/15/2013",
    "type": "IPSUM",
    "message": "LIGULA SUSPENDISSE ORNARE CONSEQUAT LECTUS"
}, {
    "time": "07/09/2019",
    "type": "AUGUE",
    "message": "NON VELIT NEC NISI"
}, {
    "time": "08/05/2019",
    "type": "EGET",
    "message": "JUSTO IN HAC HABITASSE PLATEA DICTUMST"
}, {
    "time": "08/18/2012",
    "type": "VESTIBULUM",
    "message": "IPSUM DOLOR SIT AMET CONSECTETUER"
}, {
    "time": "04/01/2019",
    "type": "MAURIS",
    "message": "DONEC PHARETRA MAGNA VESTIBULUM ALIQUET ULTRICES ERAT"
}, {
    "time": "09/15/2016",
    "type": "FELIS",
    "message": "DOLOR VEL EST DONEC ODIO"
}, {
    "time": "06/16/2017",
    "type": "PORTTITOR",
    "message": "COMMODO PLACERAT PRAESENT BLANDIT NAM"
}, {
    "time": "08/03/2018",
    "type": "ETIAM",
    "message": "ALIQUAM ERAT VOLUTPAT IN CONGUE ETIAM"
}, {
    "time": "12/16/2011",
    "type": "LACINIA",
    "message": "MATTIS PULVINAR NULLA PEDE"
}, {
    "time": "07/08/2015",
    "type": "CONVALLIS",
    "message": "A NIBH IN QUIS"
}, {
    "time": "02/10/2017",
    "type": "HABITASSE",
    "message": "VEL AUGUE VESTIBULUM RUTRUM RUTRUM NEQUE"
}, {
    "time": "06/03/2014",
    "type": "MAURIS",
    "message": "SIT AMET TURPIS ELEMENTUM LIGULA VEHICULA CONSEQUAT"
}, {
    "time": "12/20/2015",
    "type": "MALESUADA",
    "message": "SIT AMET LOBORTIS SAPIEN SAPIEN NON"
}, {
    "time": "12/03/2014",
    "type": "ET",
    "message": "QUAM SAPIEN VARIUS UT BLANDIT"
}, {
    "time": "08/08/2020",
    "type": "ENIM",
    "message": "NAM CONGUE RISUS SEMPER PORTA"
}, {
    "time": "05/18/2018",
    "type": "ERAT",
    "message": "AUCTOR SED TRISTIQUE IN TEMPUS SIT AMET"
}, {
    "time": "02/16/2020",
    "type": "LOBORTIS",
    "message": "PEDE VENENATIS NON SODALES SED"
}, {
    "time": "07/04/2016",
    "type": "INTEGER",
    "message": "NEC CONDIMENTUM NEQUE SAPIEN PLACERAT"
}, {
    "time": "05/06/2013",
    "type": "VEL",
    "message": "IPSUM AC TELLUS SEMPER INTERDUM"
}, {
    "time": "04/13/2016",
    "type": "INTEGER",
    "message": "ELEMENTUM PELLENTESQUE QUISQUE PORTA VOLUTPAT ERAT"
}, {
    "time": "03/24/2015",
    "type": "DONEC",
    "message": "SODALES SCELERISQUE MAURIS SIT AMET EROS SUSPENDISSE"
}, {
    "time": "11/21/2014",
    "type": "A",
    "message": "EROS SUSPENDISSE ACCUMSAN TORTOR QUIS"
}, {
    "time": "03/13/2016",
    "type": "ETIAM",
    "message": "NIBH FUSCE LACUS PURUS ALIQUET"
}, {
    "time": "01/01/2015",
    "type": "IMPERDIET",
    "message": "EUISMOD SCELERISQUE QUAM TURPIS ADIPISCING LOREM VITAE"
}, {
    "time": "02/12/2011",
    "type": "SUSPENDISSE",
    "message": "TURPIS EGET ELIT SODALES SCELERISQUE MAURIS"
}, {
    "time": "08/12/2016",
    "type": "VESTIBULUM",
    "message": "LUCTUS ET ULTRICES POSUERE CUBILIA CURAE MAURIS"
}, {
    "time": "10/23/2010",
    "type": "URNA",
    "message": "DONEC DAPIBUS DUIS AT VELIT"
}, {
    "time": "08/23/2018",
    "type": "LIGULA",
    "message": "RHONCUS ALIQUET PULVINAR SED"
}, {
    "time": "02/09/2015",
    "type": "NUNC",
    "message": "VENENATIS TURPIS ENIM BLANDIT MI IN"
}, {
    "time": "04/05/2011",
    "type": "NIBH",
    "message": "ULTRICES LIBERO NON MATTIS"
}, {
    "time": "05/05/2014",
    "type": "NEQUE",
    "message": "TEMPUS VEL PEDE MORBI PORTTITOR LOREM ID"
}, {
    "time": "05/26/2016",
    "type": "NIBH",
    "message": "PRAESENT BLANDIT LACINIA ERAT"
}, {
    "time": "06/16/2015",
    "type": "ULLAMCORPER",
    "message": "AMET LOBORTIS SAPIEN SAPIEN NON"
}, {
    "time": "01/24/2011",
    "type": "PEDE",
    "message": "UT ERAT CURABITUR GRAVIDA NISI"
}, {
    "time": "09/17/2013",
    "type": "LACUS",
    "message": "INTEGER AC LEO PELLENTESQUE ULTRICES"
}, {
    "time": "12/17/2015",
    "type": "CONGUE",
    "message": "BLANDIT LACINIA ERAT"
}, {
    "time": "06/06/2015",
    "type": "SEMPER",
    "message": "MOLESTIE NIBH IN LECTUS PELLENTESQUE AT"
}, {
    "time": "08/03/2014",
    "type": "ULLAMCORPER",
    "message": "MONTES NASCETUR RIDICULUS MUS ETIAM VEL AUGUE"
}, {
    "time": "07/01/2016",
    "type": "ETIAM",
    "message": "BLANDIT NON INTERDUM IN ANTE VESTIBULUM ANTE"
}, {
    "time": "05/31/2016",
    "type": "ULTRICES",
    "message": "ELEMENTUM EU INTERDUM EU TINCIDUNT IN"
}, {
    "time": "08/03/2020",
    "type": "IN",
    "message": "DONEC UT MAURIS EGET MASSA"
}, {
    "time": "10/07/2015",
    "type": "PROIN",
    "message": "EU NIBH QUISQUE ID JUSTO SIT"
}, {
    "time": "06/08/2014",
    "type": "ORCI",
    "message": "NULLAM MOLESTIE NIBH IN LECTUS"
}, {
    "time": "06/13/2016",
    "type": "ID",
    "message": "PLATEA DICTUMST MAECENAS UT MASSA QUIS AUGUE"
}, {
    "time": "08/20/2014",
    "type": "METUS",
    "message": "FELIS SED INTERDUM VENENATIS"
}, {
    "time": "01/08/2016",
    "type": "NUNC",
    "message": "ETIAM FAUCIBUS CURSUS URNA"
}, {
    "time": "02/22/2020",
    "type": "NISI",
    "message": "JUSTO ALIQUAM QUIS TURPIS EGET ELIT SODALES"
}, {
    "time": "02/11/2012",
    "type": "CURABITUR",
    "message": "LACUS AT TURPIS DONEC POSUERE METUS VITAE"
}, {
    "time": "07/21/2018",
    "type": "CUBILIA",
    "message": "POSUERE METUS VITAE IPSUM ALIQUAM"
}, {
    "time": "11/30/2011",
    "type": "IN",
    "message": "PEDE POSUERE NONUMMY INTEGER NON"
}, {
    "time": "03/26/2013",
    "type": "PEDE",
    "message": "METUS VITAE IPSUM ALIQUAM NON"
}, {
    "time": "04/24/2020",
    "type": "TELLUS",
    "message": "EU FELIS FUSCE"
}, {
    "time": "06/23/2015",
    "type": "LACINIA",
    "message": "A IPSUM INTEGER A NIBH IN QUIS"
}, {
    "time": "03/10/2019",
    "type": "CONVALLIS",
    "message": "MALESUADA IN IMPERDIET ET COMMODO VULPUTATE"
}, {
    "time": "04/17/2018",
    "type": "NON",
    "message": "ID LUCTUS NEC MOLESTIE SED JUSTO PELLENTESQUE"
}, {
    "time": "03/14/2020",
    "type": "PORTA",
    "message": "NULLA EGET EROS ELEMENTUM"
}, {
    "time": "04/27/2019",
    "type": "CONSEQUAT",
    "message": "IN PURUS EU MAGNA VULPUTATE"
}, {
    "time": "12/21/2012",
    "type": "ANTE",
    "message": "NULLA MOLLIS MOLESTIE LOREM QUISQUE UT ERAT"
}, {
    "time": "10/14/2013",
    "type": "CONSEQUAT",
    "message": "TELLUS NULLA UT ERAT ID MAURIS VULPUTATE"
}, {
    "time": "12/04/2015",
    "type": "EGET",
    "message": "MI IN PORTTITOR PEDE JUSTO EU MASSA"
}, {
    "time": "02/15/2016",
    "type": "JUSTO",
    "message": "EGET TEMPUS VEL PEDE MORBI PORTTITOR"
}, {
    "time": "06/16/2013",
    "type": "ARCU",
    "message": "QUAM PEDE LOBORTIS"
}, {
    "time": "10/17/2016",
    "type": "SAPIEN",
    "message": "IN PORTTITOR PEDE JUSTO EU"
}, {
    "time": "05/24/2016",
    "type": "FELIS",
    "message": "MASSA QUIS AUGUE LUCTUS TINCIDUNT NULLA"
}, {
    "time": "04/16/2012",
    "type": "QUAM",
    "message": "DIAM NAM TRISTIQUE TORTOR EU PEDE"
}, {
    "time": "08/02/2020",
    "type": "PEDE",
    "message": "SAGITTIS NAM CONGUE RISUS SEMPER PORTA VOLUTPAT"
}, {
    "time": "07/04/2012",
    "type": "EGET",
    "message": "SED VESTIBULUM SIT"
}, {
    "time": "07/07/2019",
    "type": "CONGUE",
    "message": "SIT AMET JUSTO"
}, {
    "time": "08/11/2020",
    "type": "ET",
    "message": "AT TURPIS DONEC POSUERE"
}, {
    "time": "11/03/2012",
    "type": "MORBI",
    "message": "MAECENAS RHONCUS ALIQUAM"
}, {
    "time": "07/21/2014",
    "type": "JUSTO",
    "message": "SEM MAURIS LAOREET UT RHONCUS"
}, {
    "time": "04/27/2012",
    "type": "SED",
    "message": "ET EROS VESTIBULUM"
}, {
    "time": "02/13/2019",
    "type": "ERAT",
    "message": "LECTUS PELLENTESQUE AT NULLA SUSPENDISSE POTENTI CRAS"
}, {
    "time": "12/28/2012",
    "type": "EGET",
    "message": "LIGULA PELLENTESQUE ULTRICES PHASELLUS ID SAPIEN"
}, {
    "time": "06/22/2016",
    "type": "VESTIBULUM",
    "message": "AC ENIM IN TEMPOR"
}, {
    "time": "05/05/2016",
    "type": "VOLUTPAT",
    "message": "LOREM IPSUM DOLOR SIT AMET"
}, {
    "time": "01/04/2015",
    "type": "LOREM",
    "message": "ULTRICES PHASELLUS ID SAPIEN IN SAPIEN IACULIS"
}, {
    "time": "09/04/2017",
    "type": "RISUS",
    "message": "UT ERAT CURABITUR GRAVIDA NISI"
}, {
    "time": "04/09/2018",
    "type": "SOCIIS",
    "message": "SIT AMET LOBORTIS SAPIEN"
}, {
    "time": "05/31/2011",
    "type": "POSUERE",
    "message": "CONVALLIS NULLA NEQUE LIBERO CONVALLIS EGET ELEIFEND"
}, {
    "time": "11/18/2016",
    "type": "VESTIBULUM",
    "message": "NULLA ULTRICES ALIQUET MAECENAS"
}, {
    "time": "02/04/2011",
    "type": "RHONCUS",
    "message": "DOLOR QUIS ODIO"
}, {
    "time": "05/21/2019",
    "type": "MI",
    "message": "VARIUS INTEGER AC LEO PELLENTESQUE"
}, {
    "time": "07/18/2016",
    "type": "IACULIS",
    "message": "PEDE LIBERO QUIS ORCI"
}, {
    "time": "02/04/2017",
    "type": "ARCU",
    "message": "FAUCIBUS CURSUS URNA"
}, {
    "time": "03/13/2017",
    "type": "PHARETRA",
    "message": "FAUCIBUS ACCUMSAN ODIO CURABITUR CONVALLIS DUIS"
}, {
    "time": "12/23/2012",
    "type": "VITAE",
    "message": "TURPIS ENIM BLANDIT MI IN PORTTITOR PEDE"
}]

const columns = [
    {
        title: "Time",
        data_row_name: "time",
        title_props: { align: "center" },
        data_row_props: { align: "center", component: "th", scope: "row" }
    },
    {
        title: "Type",
        data_row_name: "type",
        title_props: { align: "center" },
        data_row_props: { align: "center" }
    },
    {
        title: "Message",
        data_row_name: "message",
        title_props: { align: "right" },
        data_row_props: { align: "right" }
    }
]

export default function Home() {

    const [messages, setMessages] = useState(test_data)


    function getMessages() {
        console.log("refresh messages");
    }

    return (
        <>
            <Row className="w-100 p-0 m-0">
                <Col className="p-0"><Typography variant="h5">Running Messages:</Typography></Col>
                <Col className="p-0 d-flex justify-content-end">
                    <ReloadButtonComponent reloadDataFunc={getMessages} />
                </Col>
            </Row>
            <br />

            <SuricataTableComponent columns={columns} data={messages} />

        </>
    )
}