
void FUN__text__004da450(short *param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (int)*param_1;
  local_8 = FUN__text__004da5f0(local_c);
  FUN__text__004dfc20(local_8,param_2);
  *(char *)(param_2 + 0xf) = (char)param_1[1];
  *(undefined1 *)(param_2 + 0x94) = *(undefined1 *)((int)param_1 + 3);
  *(char *)(param_2 + 0x96) = (char)param_1[2];
  *(undefined1 *)(param_2 + 0x97) = *(undefined1 *)((int)param_1 + 5);
  *(char *)(param_2 + 0x98) = (char)param_1[3];
  *(undefined1 *)(param_2 + 0x9b) = *(undefined1 *)((int)param_1 + 7);
  *(char *)(param_2 + 0x9c) = (char)param_1[4];
  *(undefined1 *)(param_2 + 0x9d) = *(undefined1 *)((int)param_1 + 9);
  *(char *)(param_2 + 0x9e) = (char)param_1[5];
  *(undefined1 *)(param_2 + 0x9f) = *(undefined1 *)((int)param_1 + 0xb);
  *(char *)(param_2 + 0xa0) = (char)param_1[6];
  *(undefined1 *)(param_2 + 0xa2) = *(undefined1 *)((int)param_1 + 0xd);
  *(char *)(param_2 + 0xa3) = (char)param_1[7];
  *(short *)(param_2 + 0xa8) = param_1[8];
  if ((((*(char *)((int)param_1 + 3) != '\0') && (*(char *)((int)param_1 + 3) != '\x04')) &&
      (*(char *)((int)param_1 + 3) != '\x05')) &&
     ((*(char *)((int)param_1 + 3) != '\x06' && (*(char *)((int)param_1 + 3) != '\a')))) {
    iVar2 = FUN__text__00424f80("(0==tbl->user) || (4==tbl->user) || (5==tbl->user) || (6==tbl->user) || (7==tbl->user)"
                                ,"e:\\crosshermit\\game\\src\\common\\comenemy.cpp",
                                DAT_006a88cc + 0x1c,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(undefined1 *)(param_2 + 0xa4) = *(undefined1 *)((int)param_1 + 3);
  local_8 = 0x4da5e1;
  FUN__text__0056ce80();
  return;
}

