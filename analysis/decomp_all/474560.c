
void FUN__text__00474560(undefined2 *param_1,char *param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__0042b2d0("***********************\n ",param_3);
  FUN__text__0042b2d0("no\t\t\t\t\t= %d\n ",*param_1);
  FUN__text__0042b2d0("wk->no\t\t\t\t= %d\n ",param_1[1]);
  FUN__text__0042b2d0("wk->char_no\t\t= %d\n ",*(undefined1 *)(param_1 + 2));
  FUN__text__0042b2d0("wk->c_str\t\t\t= %d\n ",*(undefined1 *)((int)param_1 + 5));
  FUN__text__0042b2d0("wk->c_agi\t\t\t= %d\n ",*(undefined1 *)(param_1 + 3));
  FUN__text__0042b2d0("wk->c_sen\t\t\t= %d\n ",*(undefined1 *)((int)param_1 + 7));
  FUN__text__0042b2d0("wk->c_vir\t\t\t= %d\n ",*(undefined1 *)(param_1 + 4));
  FUN__text__0042b2d0("wk->c_int\t\t\t= %d\n ",*(undefined1 *)((int)param_1 + 9));
  FUN__text__0042b2d0("wk->c_con\t\t\t= %d\n ",*(undefined1 *)(param_1 + 5));
  FUN__text__0042b2d0("wk->c_spi\t\t\t= %d\n ",param_1[6]);
  FUN__text__0042b2d0("wk->job\t\t\t= %d\n ",*(undefined1 *)(param_1 + 7));
  FUN__text__0042b2d0("wk->level\t\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0xf));
  FUN__text__0042b2d0("wk->dead\t\t\t= %d\n ",param_1[8]);
  FUN__text__0042b2d0("wk->force_val\t\t= %d\n ",param_1[9]);
  FUN__text__0042b2d0("wk->force\t\t\t= %d\n ",(int)(short)param_1[10]);
  FUN__text__0042b2d0("wk->hp_max\t\t\t= %d\n ",(int)(short)param_1[0xb]);
  FUN__text__0042b2d0("wk->hp\t\t\t\t= %d\n ",(int)(short)param_1[0xc]);
  FUN__text__0042b2d0("wk->hp_healing\t\t= %d\n ",(int)(short)param_1[0xd]);
  FUN__text__0042b2d0("wk->mp_max\t\t\t= %d\n ",(int)(short)param_1[0xe]);
  FUN__text__0042b2d0("wk->mp\t\t\t\t= %d\n ",(int)(short)param_1[0xf]);
  FUN__text__0042b2d0("wk->mp_healing\t\t= %d\n ",*(undefined4 *)(param_1 + 0x10));
  FUN__text__0042b2d0("wk->alt_max\t\t= %d\n ",*(undefined4 *)(param_1 + 0x12));
  FUN__text__0042b2d0("wk->alt\t\t\t= %d\n ",*(undefined4 *)(param_1 + 0x14));
  FUN__text__0042b2d0("wk->alt_tuning\t\t= %d\n ",*(undefined1 *)(param_1 + 0x16));
  FUN__text__0042b2d0("wk->view\t\t\t= %d\n ",param_1[0x17]);
  FUN__text__0042b2d0("wk->move\t\t\t= %d\n ",*(undefined1 *)(param_1 + 0x18));
  FUN__text__0042b2d0("wk->move_type\t\t= %d\n ",param_1[0x19]);
  FUN__text__0042b2d0("wk->ready\t\t\t= %d\n ",param_1[0x1a]);
  FUN__text__0042b2d0("wk->stiff\t\t\t= %d\n ",*(undefined1 *)(param_1 + 0x1b));
  FUN__text__0042b2d0("wk->range_min\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x37));
  FUN__text__0042b2d0("wk->range\t\t\t= %d\n ",param_1[0x1c]);
  FUN__text__0042b2d0("wk->dex\t\t\t= %d\n ",param_1[0x1d]);
  FUN__text__0042b2d0("wk->str_min\t\t= %d\n ",param_1[0x1e]);
  FUN__text__0042b2d0("wk->str_range\t\t= %d\n ",param_1[0x1f]);
  FUN__text__0042b2d0("wk->skill_fact\t\t= %d\n ",*(undefined1 *)(param_1 + 0x20));
  FUN__text__0042b2d0("wk->skill_type\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x41));
  FUN__text__0042b2d0("wk->spefct_per\t\t= %d\n ",param_1[0x21]);
  FUN__text__0042b2d0("wk->extra_mighty\t= %d\n ",*(undefined1 *)(param_1 + 0x22));
  FUN__text__0042b2d0("wk->efct_range\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x45));
  FUN__text__0042b2d0("wk->sp_efct\t\t= %d\n ",*(undefined4 *)(param_1 + 0x24));
  FUN__text__0042b2d0("wk->efct_time\t\t= %d\n ",*(undefined1 *)(param_1 + 0x26));
  FUN__text__0042b2d0("wk->agl\t\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x4d));
  FUN__text__0042b2d0("wk->def\t\t\t= %d\n ",*(undefined1 *)(param_1 + 0x27));
  FUN__text__0042b2d0("wk->body\t\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x4f));
  FUN__text__0042b2d0("wk->magic\t\t\t= %d\n ",*(undefined1 *)(param_1 + 0x28));
  FUN__text__0042b2d0("wk->mental\t\t\t= %d\n ",param_1[0x29]);
  FUN__text__0042b2d0("wk->damage\t\t\t= %d\n ",param_1[0x2a]);
  FUN__text__0042b2d0("wk->dead_def\t\t= %d\n ",*(undefined1 *)(param_1 + 0x2b));
  FUN__text__0042b2d0("wk->bcon_type\t\t= %d\n ",param_1[0x2c]);
  FUN__text__0042b2d0("wk->bcon_unit\t\t= %d\n ",param_1[0x2d]);
  FUN__text__0042b2d0("wk->bcon_skill\t\t= %d\n ",*(undefined4 *)(param_1 + 0x2e));
  FUN__text__0042b2d0("wk->bcon_time\t\t= %d\n ",*(undefined1 *)(param_1 + 0x30));
  FUN__text__0042b2d0("wk->bcon_view\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x61));
  FUN__text__0042b2d0("wk->bcon_move\t\t= %d\n ",*(undefined1 *)(param_1 + 0x31));
  FUN__text__0042b2d0("wk->bcon_atk\t\t= %d\n ",*(undefined1 *)((int)param_1 + 99));
  FUN__text__0042b2d0("wk->bcon_def\t\t= %d\n ",*(undefined1 *)(param_1 + 0x32));
  FUN__text__0042b2d0("wk->bcon_mag\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x65));
  FUN__text__0042b2d0("wk->scon_type\t\t= %d\n ",param_1[0x33]);
  FUN__text__0042b2d0("wk->scon_unit\t\t= %d\n ",param_1[0x34]);
  FUN__text__0042b2d0("wk->scon_skill\t\t= %d\n ",*(undefined4 *)(param_1 + 0x36));
  FUN__text__0042b2d0("wk->scon_time\t\t= %d\n ",*(undefined1 *)(param_1 + 0x38));
  FUN__text__0042b2d0("wk->gcon_type\t\t= %d\n ",param_1[0x39]);
  FUN__text__0042b2d0("wk->gcon_unit\t\t= %d\n ",param_1[0x3a]);
  FUN__text__0042b2d0("wk->gcon_skill\t\t= %d\n ",*(undefined4 *)(param_1 + 0x3c));
  FUN__text__0042b2d0("wk->gcon_etime\t\t= %d\n ",*(undefined1 *)(param_1 + 0x3e));
  FUN__text__0042b2d0("wk->gcon_stime\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x7d));
  FUN__text__0042b2d0("wk->gcon_view\t\t= %d\n ",*(undefined1 *)(param_1 + 0x3f));
  FUN__text__0042b2d0("wk->gcon_move\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x7f));
  FUN__text__0042b2d0("wk->gcon_oself\t\t= %d\n ",*(undefined4 *)(param_1 + 0x40));
  FUN__text__0042b2d0("wk->gcon_htime\t\t= %d\n ",param_1[0x42]);
  FUN__text__0042b2d0("wk->pocket[0]\t\t= %d\n ",param_1[0x43]);
  FUN__text__0042b2d0("wk->pocket[1]\t\t= %d\n ",param_1[0x44]);
  FUN__text__0042b2d0("wk->pocket[2]\t\t= %d\n ",param_1[0x45]);
  FUN__text__0042b2d0("wk->pocket[3]\t\t= %d\n ",param_1[0x46]);
  FUN__text__0042b2d0("wk->pocket[4]\t\t= %d\n ",param_1[0x47]);
  FUN__text__0042b2d0("wk->pocket[5]\t\t= %d\n ",param_1[0x48]);
  FUN__text__0042b2d0("wk->pocket[6]\t\t= %d\n ",param_1[0x49]);
  FUN__text__0042b2d0("wk->pocket[7]\t\t= %d\n ",*(undefined1 *)(param_1 + 0x4a));
  FUN__text__0042b2d0("wk->user\t\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x95));
  FUN__text__0042b2d0("wk->powerful\t\t= %d\n ",*(undefined1 *)(param_1 + 0x4b));
  FUN__text__0042b2d0("wk->unit_type\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x97));
  FUN__text__0042b2d0("wk->child_cnt\t\t= %d\n ",*(undefined1 *)(param_1 + 0x4c));
  FUN__text__0042b2d0("wk->group\t\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x99));
  FUN__text__0042b2d0("wk->post\t\t\t= %d\n ",*(undefined1 *)(param_1 + 0x4d));
  FUN__text__0042b2d0("wk->faction\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x9b));
  FUN__text__0042b2d0("wk->scx\t\t\t= %d\n ",*(undefined1 *)(param_1 + 0x4e));
  FUN__text__0042b2d0("wk->scy\t\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x9d));
  FUN__text__0042b2d0("wk->atk_mode\t\t= %d\n ",*(undefined1 *)(param_1 + 0x4f));
  FUN__text__0042b2d0("wk->now_skill\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0x9f));
  FUN__text__0042b2d0("wk->ai_atk\t\t\t= %d\n ",*(undefined1 *)(param_1 + 0x50));
  FUN__text__0042b2d0("wk->ai_act\t\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0xa1));
  FUN__text__0042b2d0("wk->ai_type\t\t= %d\n ",*(undefined1 *)(param_1 + 0x51));
  FUN__text__0042b2d0("wk->route_no\t\t= %d\n ",*(undefined1 *)((int)param_1 + 0xa3));
  FUN__text__0042b2d0("wk->event_flag\t\t= %d\n ",*(undefined1 *)(param_1 + 0x52));
  FUN__text__0042b2d0("wk->player\t\t\t= %d\n ");
  FUN__text__0042b2d0(&DAT_0059cacc);
  FUN__text__0042b2d0("move_type\t\t\t= %d\n ",(int)*param_2);
  FUN__text__0042b2d0("no_path\t\t\t= %d\n ",(int)param_2[1]);
  FUN__text__0042b2d0("move_time\t\t\t= %d\n ",*(undefined4 *)(param_2 + 4));
  FUN__text__0042b2d0("move_stime\t\t\t= %d\n ",*(undefined4 *)(param_2 + 8));
  FUN__text__0042b2d0("search_time\t\t= %d\n ",*(undefined4 *)(param_2 + 0xc));
  FUN__text__0042b2d0("search_kind\t\t= %d\n ",(int)param_2[0x10]);
  FUN__text__0042b2d0("search_cond\t\t= %d\n ",(int)param_2[0x11]);
  FUN__text__0042b2d0("serach_result\t\t= %d\n ",(int)param_2[0x12]);
  FUN__text__0042b2d0("serach_fickle\t\t= %d\n ",(int)param_2[0x13]);
  FUN__text__0042b2d0("serach_missing\t\t= %d\n ",(int)param_2[0x14]);
  FUN__text__0042b2d0("missing_after\t\t= %d\n ",(int)param_2[0x15]);
  FUN__text__0042b2d0("missing_setpos\t\t= %d\n ",(int)param_2[0x16]);
  FUN__text__0042b2d0("attack_kind\t\t= %d\n ",(int)param_2[0x19]);
  FUN__text__0042b2d0("attack_skill\t\t= %d\n ",(int)param_2[0x1a]);
  FUN__text__0042b2d0("attack_serach\t\t= %d\n ",(int)param_2[0x1b]);
  FUN__text__0042b2d0("attack_base\t\t= %d\n ",(int)param_2[0x1c]);
  FUN__text__0042b2d0("counter_attack\t\t= %d\n ",(int)param_2[0x1e]);
  FUN__text__0042b2d0("call_time\t\t\t= %d\n ",*(undefined4 *)(param_2 + 0x20));
  FUN__text__0042b2d0(&DAT_0059cacc);
  local_8 = 0x474fa1;
  FUN__text__0056ce80();
  return;
}

