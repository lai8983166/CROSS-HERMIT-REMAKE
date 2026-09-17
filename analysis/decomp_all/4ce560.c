
void __thiscall FUN__text__004ce560(int param_1,uint param_2,int param_3)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  uint local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *(undefined1 *)(param_1 + 0x1cc) = 0xff;
  *(undefined1 *)(param_1 + 0x9228) = 1;
  local_8 = param_1;
  uVar1 = FUN__text__004cd700(*(undefined4 *)(param_1 + 0xc + (param_2 & 0xffff) * 0x1c8),0);
  *(undefined4 *)(local_8 + 0x10 + (param_2 & 0xffff) * 0x1c8) = uVar1;
  uVar1 = FUN__text__004cd700(*(undefined4 *)(local_8 + 0xc + (param_2 & 0xffff) * 0x1c8),1);
  *(undefined4 *)(local_8 + 0x14 + (param_2 & 0xffff) * 0x1c8) = uVar1;
  uVar1 = FUN__text__004cd700(*(undefined4 *)(local_8 + 0xc + (param_2 & 0xffff) * 0x1c8),2);
  *(undefined4 *)(local_8 + 0x18 + (param_2 & 0xffff) * 0x1c8) = uVar1;
  *(undefined1 *)(local_8 + 4 + (param_2 & 0xffff) * 0x1c8) = 1;
  *(undefined4 *)(local_8 + 0x1c + (param_2 & 0xffff) * 0x1c8) = 0;
  *(undefined2 *)(local_8 + 0x20 + (param_2 & 0xffff) * 0x1c8) = 0;
  for (local_c = 0; local_c < 0x32; local_c = local_c + 1) {
    *(undefined4 *)(local_8 + (param_2 & 0xffff) * 0x1c8 + 0x3c + local_c * 4) = 0;
  }
  if (param_3 != 0x7f) {
    *(int *)(local_8 + 0x92dc) = param_3;
  }
  local_8 = 0x4ce6da;
  FUN__text__0056ce80();
  return;
}

