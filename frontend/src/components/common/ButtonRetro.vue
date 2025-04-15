<template>
  <button
    :class="[
      'font-sans text-base tracking-widest uppercase text-black cursor-pointer border-4 py-1 px-2.5 shadow-[1px_1px_0px_0px,_2px_2px_0px_0px,_3px_3px_0px_0px,_4px_4px_0px_0px,_5px_5px_0px_0px] relative select-none focus:outline-none',
      activeClass,
      hoverClass,
      sizeClass
    ]"
    :role="role"
  >
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'ButtonRetro',
  props: {
    role: {
      type: String,
      default: 'button'
    },
    activeClass: {
      type: String,
      default: 'active:shadow-none active:top-[5px] active:left-[5px]'
    },
    hoverClass: {
      type: String,
      default: ''
    },
    sizeClass: {
      type: String,
      default: 'md:px-3 md:py-2'
    }
  }
}
</script>
