<template>
    <button :class="classesBouton" @click="$emit('press')">
        <slot />
    </button>
  </template>
  
  <script lang="ts">
  import { defineComponent, type PropType } from "vue";
  import { CouleurBouton } from "@/scripts/SpecialEnum";
  
  export default defineComponent({
    name: "BriqueButton",
    props: {
        couleur: {
            required: true,
            type: String as PropType<CouleurBouton>,
        },
    },
    data() {
      return {
        CouleurBouton: CouleurBouton,
      }
    },
    emits: {
        press: null
    },
    computed: {
        classesBouton(): string[] {
            let classesDeBase = [
            "rounded-full",
            "w-fit",
            "px-8",
             "h-10",
            "flex",
            "font-bold",
            "items-center",
            "align-center",
            "justify-center",
             "transition-all",
            "duration-300",
            "mx-2"
            ];

            switch (this.couleur) {
                case CouleurBouton.Mauve:
                classesDeBase.push("bg-BbLightPurple", "hover:bg-BbPurple","text-trempanilloWhite");
                    break;
                case CouleurBouton.Jaune:
                classesDeBase.push("bg-trempanilloBeigePale", "hover:bg-trempanilloBeige","text-trempanilloDarkBlue");
                    break;
                case CouleurBouton.Orange:
                classesDeBase.push("bg-trempanilloBeige", "hover:bg-trempanilloDarkYellow","text-trempanilloWhite");
                    break;
                case CouleurBouton.OrangeBeige:
                classesDeBase.push("bg-trempanilloBeige", "hover:bg-trempanilloBeigePale","text-trempanilloDarkBlue");
                    break;
            }
            return classesDeBase;
        },
  }
});

  </script>
  