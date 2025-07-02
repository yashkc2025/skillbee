<script setup lang="tsx">
const props = withDefaults(defineProps<{
  maxItems?: number;
  showExpand?: boolean;
}>(), {
  showExpand: false,
})

import CardV2 from "@/components/CardV2.vue";
import InputComponent from "@/components/InputComponent.vue";
import TableComponent from "@/components/TableComponent.vue";
import { useRouter } from "vue-router";
import sitemap from "@/router/sitemap.json"


const children = [
  {
    id: 1,
    name: "Yash K",
    email: "yash.kumar@app.com",
    age: 10,
    school_name: "Greenwood High",
    last_login: "July 1, 2025 2:30 PM",
  },
  {
    id: 2,
    name: "Aarav Sharma",
    email: "aarav.sharma@app.com",
    age: 11,
    school_name: "Delhi Public School",
    last_login: "July 2, 2025 8:45 AM",
  },
  {
    id: 3,
    name: "Isha Reddy",
    email: "isha.reddy@app.com",
    age: 9,
    school_name: "Oakridge International",
    last_login: "June 30, 2025 5:15 PM",
  },
  {
    id: 4,
    name: "Rohan Mehta",
    email: "rohan.mehta@app.com",
    age: 12,
    school_name: "National Public School",
    last_login: "July 2, 2025 10:00 AM",
  },
  {
    id: 5,
    name: "Tanvi Verma",
    email: "tanvi.verma@app.com",
    age: 10,
    school_name: "Vidya Mandir",
    last_login: "July 1, 2025 1:20 PM",
  },
  {
    id: 6,
    name: "Kavya Nair",
    email: "kavya.nair@app.com",
    age: 11,
    school_name: "The International School",
    last_login: "July 2, 2025 9:10 AM",
  },
  {
    id: 7,
    name: "Aryan Patel",
    email: "aryan.patel@app.com",
    age: 10,
    school_name: "St. Xavier's High School",
    last_login: "June 29, 2025 3:40 PM",
  },
  {
    id: 8,
    name: "Meera Joshi",
    email: "meera.joshi@app.com",
    age: 12,
    school_name: "Ryan International School",
    last_login: "July 1, 2025 11:05 AM",
  },
  {
    id: 9,
    name: "Devansh Singh",
    email: "devansh.singh@app.com",
    age: 9,
    school_name: "Modern School",
    last_login: "July 2, 2025 7:50 AM",
  },
  {
    id: 10,
    name: "Anika Kapoor",
    email: "anika.kapoor@app.com",
    age: 10,
    school_name: "Springdales School",
    last_login: "June 28, 2025 6:00 PM",
  },
  {
    id: 11,
    name: "Reyansh Das",
    email: "reyansh.das@app.com",
    age: 11,
    school_name: "Heritage School",
    last_login: "July 2, 2025 8:30 AM",
  },
  {
    id: 12,
    name: "Saanvi Iyer",
    email: "saanvi.iyer@app.com",
    age: 9,
    school_name: "Baldwin Girls' High School",
    last_login: "July 1, 2025 12:45 PM",
  },
  {
    id: 13,
    name: "Neil Desai",
    email: "neil.desai@app.com",
    age: 12,
    school_name: "DAV Public School",
    last_login: "June 30, 2025 4:25 PM",
  },
  {
    id: 14,
    name: "Aanya Mukherjee",
    email: "aanya.mukherjee@app.com",
    age: 10,
    school_name: "La Martiniere for Girls",
    last_login: "July 2, 2025 9:55 AM",
  },
  {
    id: 15,
    name: "Vivaan Bhatt",
    email: "vivaan.bhatt@app.com",
    age: 11,
    school_name: "Glendale Academy",
    last_login: "June 27, 2025 5:10 PM",
  },
  {
    id: 16,
    name: "Riya Malhotra",
    email: "riya.malhotra@app.com",
    age: 9,
    school_name: "Presidency School",
    last_login: "July 1, 2025 2:00 PM",
  },
  {
    id: 17,
    name: "Arjun Chauhan",
    email: "arjun.chauhan@app.com",
    age: 10,
    school_name: "Sanskriti School",
    last_login: "July 2, 2025 7:15 AM",
  },
  {
    id: 18,
    name: "Diya Sinha",
    email: "diya.sinha@app.com",
    age: 12,
    school_name: "Bishop Cotton Girls' School",
    last_login: "June 30, 2025 3:30 PM",
  },
  {
    id: 19,
    name: "Mohit Agarwal",
    email: "mohit.agarwal@app.com",
    age: 11,
    school_name: "Shiv Nadar School",
    last_login: "July 2, 2025 8:20 AM",
  },
  {
    id: 20,
    name: "Sneha Pillai",
    email: "sneha.pillai@app.com",
    age: 10,
    school_name: "DPS Whitefield",
    last_login: "July 1, 2025 10:10 AM",
  },
];


const childrenLabel = ["ID", "Name", "Email", "Age", "School Name", "Last Login", "View More"];

const router = useRouter()

function expandTable() {
  router.push(sitemap.admin.user_management.children)
}

function navToProfile(id: number) {
  router.push({ name: 'child_profile_admin', params: { id } })
}

function tableEntries() {
  children.forEach((p) => {
    // p.blocked = <span class="chip pointer">{p.blocked ? "Blocked" : "Active"}</span>
    p.view_more = <i class="bi bi-patch-plus pointer" onClick={() => navToProfile(p.id)}></i>
  })
  if (props.maxItems) {
    return children.slice(0, props.maxItems)
  }

  return children
}
</script>

<template>
  <CardV2 label-title="Children" label-image="bi bi-backpack">
    <template #top-content>
      <div class="table-header">
        <InputComponent icon="bi bi-search" name="search" placeholder="Search for a student" />
        <i class="bi bi-arrows-angle-expand" @click="expandTable" v-if="showExpand"></i>
      </div>
    </template>
    <template #content>
      <TableComponent :header="childrenLabel" :rows="tableEntries()" />
    </template>
  </CardV2>
</template>

<style scope>
.table-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--size-xs);
}

.table-header>i {
  font-size: var(--font-sm);
  font-weight: 500;
  cursor: pointer;
  font-size: 12px;
  /* background-color: var(--color-background); */
  border: 1px solid var(--color-border);
  padding: 5px 7px;
  border-radius: var(--border-radius);
}
</style>
