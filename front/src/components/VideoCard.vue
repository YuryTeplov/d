<template>
    <div class="video-item">
        <a :href="video.youtube_url" target="_blank">
            <img :src="video.thumbnail_url" alt="Thumbnail">
        </a>
        <div class="video-info">
            <h3>{{ video.title }}</h3>
            <p>{{ video.description }}</p>
        </div>
        <button class="like-button" @click="toggleLike()">
            {{video.liked?'unlike':'like'}}
        </button>
    </div>
</template>

<script>
export default {
    data() {return {
        like_disabled: false,
    }},
    methods: {
        async toggleLike() {
            try {
                this.like_disabled = true

                if (this.video.liked) {
                    await this.$axios.delete(`/api/likes/${this.video.id}/`)
                } else {
                    await this.$axios.post('/api/likes/', {video_id: this.video.id})
                }

                this.video.liked = !this.video.liked

            } catch (error) {
                console.error(error)
            } finally {
                this.like_disabled = true
            }
        },
    },
    props: ['video'],
}
</script>