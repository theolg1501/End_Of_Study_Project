<template>
    <div class="TopStyle">
        <div style = "display: flex;">
            <b-button @click ="AlertClicked" style="margin: 1%; margin-left: 2.5%; margin-right: 2.5%; width: 15%" variant="primary">Alert</b-button>
            <b-button @click ="showOldParametersPopUp = true" style="margin: 1%; margin-left: 2.5%; margin-right: 2.5%; width: 15%" variant="secondary">Old_Parameters</b-button>
            <OldParameters v-if="showOldParametersPopUp" @close="closeOldParameters">
            </OldParameters>
            <!-- <b-button @click ="showChooseParameters = true" style="margin: 1%; margin-left: 2.5%; margin-right: 2.5%; width: 15%" variant="secondary">Parameters</b-button> -->
            <ChooseParameters v-if="showChooseParameters" @close="closeChooseParameters">
            </ChooseParameters>
            <!-- <b-form-input style="width: 5%; height: 20%; margin-top:1%" disable = "True" v-model="value" size="lg"></b-form-input> -->
            <b-button @click="showMap= !showMap" style="margin: 1%; margin-left: 2.5%; margin-right: 2.5%; width: 15%" variant="danger">Show Map</b-button>
            <Maps v-if="showMap" @close="closeMap"></Maps>
            <b-button @click ="connectDrone" style="margin: 1%; margin-left: 2.5%; margin-right: 2.5%; width: 15%" variant="success">Connect Drone</b-button>
            
            <b-button @click="showFlightPlan= !showFlightPlan" style="margin: 1%; margin-left: 2.5%; margin-right: 2.5%; width: 15%" variant="danger">Make a Flight Plan</b-button>
            <FlightPlan v-if="showFlightPlan" @close="closeFlightPlan"></FlightPlan>

            <b-button @click="showPerimeterPicture= !showPerimeterPicture" style="margin: 1%; margin-left: 2.5%; margin-right: 2.5%; width: 15%" variant="danger">Perimeter Picture</b-button>
            <PerimeterPicture v-if="showPerimeterPicture" @close="closePerimeterPicture"></PerimeterPicture>
        </div>

        <b-input-group prepend="New user" style = "margin: 1%; width:50%; margin-left: 22%; margin-top: 1%">
            <b-form-input placeholder="name here" v-model="username"></b-form-input>
            <b-form-input placeholder="age here" v-model="age"></b-form-input>
            <b-input-group-append>
            <b-button @click ="InputUsername" variant="info">Enter</b-button>
            </b-input-group-append>
        </b-input-group>

    </div>
</template>

<script>
import { onMounted, defineComponent, ref, inject} from 'vue'
import Swal from 'sweetalert2'
import OldParameters from './OldParameters.vue'
import ChooseParameters from './ChooseParameters.vue'
import Maps from './Maps.vue'
import FlightPlan from './FlightPlan.vue'
import PerimeterPicture from './PerimeterPicture.vue'

export default defineComponent({
    components: {
        OldParameters,
        ChooseParameters,
        Maps,
        FlightPlan,
        PerimeterPicture,
    },

    setup () {
        let username = ref(undefined);
        let age = ref(undefined);
        let showOldParametersPopUp = ref(false);
        let showChooseParameters = ref(false);
        let showMap = ref(false);
        let showFlightPlan = ref(false);
        let showPerimeterPicture = ref(false);
        let value = ref(undefined);
        const emitter = inject('emitter');
        let client = inject('mqttClient');
                
        onMounted(() => {
            client.on('message', (topic, message) => {
                if (topic == 'Value') {
                    value.value = message
                }
            })
        })

        function AlertClicked(){
            Swal.fire('Alert Clicked')
            //console.log("Primary Clicked !!!")
        }

        function InputUsername(){
            console.log('name: ', username.value, 'age: ', age.value)
            emitter.emit('newUser', {'name':username.value, 'age':age.value});
            username.value = undefined;
            age.value = undefined;
        }

        function closeOldParameters() {
            showOldParametersPopUp.value= false
        }

        function closeChooseParameters() {
            showChooseParameters.value= false
        }

        function closeMap() {
            showMap.value= false
        }

        function closeFlightPlan() {
            showFlightPlan.value= false
        }

        function closePerimeterPicture() {
            showPerimeterPicture.value= false
        }

        function connectDrone(){
            console.log("Clicked on 'Connect Drone'");
            client.publish('webApplication/autopilotService/connect', '');
            client.subscribe('autopilotService/webApplication/telemetryInfo');
            client.publish('webApplication/camaraService/connect', '');
        }

        return {
            AlertClicked,
            InputUsername,
            closeOldParameters,            
            closeChooseParameters,
            closeMap,
            closeFlightPlan,
            closePerimeterPicture,
            connectDrone,
            username,
            age,
            emitter,
            showOldParametersPopUp,
            showChooseParameters,
            showMap,
            showFlightPlan,
            showPerimeterPicture,
            value,
            // distances_length_and_width,
            // d_length,
            // d_width,
        }
    }
})
</script>

<style scoped>
    .TopStyle {
        border-style: solid;
        border-color: green;
        /* height: 20%; */
    }

</style>