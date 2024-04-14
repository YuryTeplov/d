<template>
    <div class="video-item">
        <a :href="video.youtube_url" target="_blank">
            <img :src="video.thumbnail_url" alt="Thumbnail">
        </a>
        <div class="video-info">
            <h3>{{ video.title }}</h3>
            <p>{{ video.description }}</p>
        </div>
        <div>
            Количество баллов для рекомендации по контенту: {{ video.similarity_score_cbf }} 
            Количество баллов для рекомендации по методу коллаборативной фильтрации: {{ video.similarity_score_cf}}
        </div>
        <button 
            class="like-button" 
            :style="{ backgroundImage: video.liked?'url(' + svgPathLikeActive + ')':'url(' + svgPathLike + ')' }" 
            :class="{ liked: video.liked }"
            @click="toggleLike()"
        >
        </button>
    </div>
</template>

<script>
import likeSvg from '@/assets/like.svg';
import activeLikeSvg from '@/assets/active_like.svg';

export default {
    data() {return {
        like_disabled: false,
        svgPathLike: likeSvg,
        svgPathLikeActive: activeLikeSvg,
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


<style lang="scss">

.like-button {
    width: 32px; /* Match SVG width */
    height: 32px; /* Match SVG height */
    background-color: black;
    background-repeat: no-repeat; /* Prevent tiling */
    background-size: cover; /* Cover the entire button area */
    background-position: center; /* Center the SVG */
    border: none; /* Remove default border */
    cursor: pointer; /* Indicate clickable area */
    transition: transform 0.2s ease; /* Smooth transition for hover effect */
}

.like-button:hover {
    transform: scale(1.1); /* Slightly increase size on hover */
}
</style>