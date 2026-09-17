
void FUN__text__0046ba10(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__0046b2c0(param_1);
  FUN__text__0043c470(*(undefined1 *)(param_1 + 0x4e7),*(undefined1 *)(param_1 + 0x4e8),0);
  *(undefined1 *)(param_1 + 0x4ea) = 0xff;
  *(undefined1 *)(param_1 + 0x4e9) = 0xff;
  *(undefined1 *)(param_1 + 0x4e5) = 0xff;
  *(undefined1 *)(param_1 + 0x4e6) = 0xff;
  if (*(int *)(param_1 + 0x518) != 0) {
    FUN__text__0048de60(param_1);
  }
  FUN__text__00493570(param_1);
  FUN__text__0040ac90(param_1 + 0x48);
  for (local_c = 0; local_c != 5; local_c = local_c + 1) {
    FUN__text__0040ac90(param_1 + 0xa0 + local_c * 0x58);
  }
  iVar1 = FUN__text__00468d80(param_1);
  if (iVar1 == 0) {
    *(undefined2 *)(param_1 + 0x4fe) = 600;
  }
  else {
    *(undefined2 *)(param_1 + 0x4fe) = 900;
  }
  *(undefined1 *)(*(int *)(param_1 + 600) + 0x9d) = 0;
  FUN__text__00492e60(param_1 + 0x4f8);
  FUN__text__00492e60(param_1 + 0x4fa);
  FUN__text__00492e60(param_1 + 0x4fc);
  FUN__text__004902a0(param_1 + 0x14);
  FUN__text__004902a0(param_1 + 0x24);
  FUN__text__004902a0(param_1 + 0x34);
  *(undefined2 *)(param_1 + 0x10) = 0;
  *(undefined2 *)(param_1 + 0x12) = 0;
  *(undefined2 *)(param_1 + 0xc) = 0;
  *(undefined2 *)(param_1 + 0xe) = 0;
  *(undefined2 *)(param_1 + 0x4e0) = 0;
  *(undefined1 *)(param_1 + 0x4e4) = 0;
  *(undefined2 *)(param_1 + 0x4ee) = 0xffff;
  *(undefined1 *)(param_1 + 0x4f0) = 0;
  *(undefined1 *)(param_1 + 0x4f1) = 0;
  *(undefined2 *)(param_1 + 0x4f2) = 0xffff;
  *(undefined2 *)(param_1 + 0x4fc) = 0;
  local_8 = 0x46bc10;
  FUN__text__0056ce80();
  return;
}

