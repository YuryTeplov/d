<template>
    <select v-model="selectedOption">
        <option v-for="option in options" :value="option.value">{{ option.label }}</option>
    </select>
</template>

<script>
export default {
    props: ['value', 'options'],
    data() {
        return {
            selectedOption: this.value
        }
    },
    watch: {
        selectedOption() {
        this.$emit('input', this.selectedOption);
        }
    }
}
</script>