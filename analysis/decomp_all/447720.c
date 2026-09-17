
void __thiscall
FUN__text__00447720(int param_1,undefined4 param_2,undefined4 param_3,int param_4,int param_5,
                   undefined2 param_6,char param_7)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_7 == -1) {
    *(undefined4 *)(param_1 + 0x94) = 0;
  }
  else {
    *(undefined4 *)(param_1 + 0x94) = 1;
  }
  *(char *)(param_1 + 0x9f) = param_7;
  *(undefined1 *)(param_1 + 0x9c) = 0x80;
  *(undefined1 *)(param_1 + 0x9d) = 0x80;
  *(undefined1 *)(param_1 + 0x9e) = 0x80;
  if (param_5 == 0) {
    *(undefined2 *)(param_1 + 0xa8) = 100;
    *(undefined2 *)(param_1 + 0xaa) = 100;
    *(undefined2 *)(param_1 + 0x90) = 200;
  }
  else {
    *(undefined2 *)(param_1 + 0xa8) = param_6;
    *(undefined2 *)(param_1 + 0xaa) = param_6;
    *(undefined2 *)(param_1 + 0x90) = 0xc9;
  }
  local_8 = param_1;
  FUN__text__004077c0(DAT_007a49fc);
  FUN__text__00407870(0x5a,6);
  *(undefined2 *)(local_8 + 0xae) = 0x54;
  *(undefined2 *)(local_8 + 0x70) = *(undefined2 *)(&DAT_00605cac + param_4 * 8);
  *(undefined2 *)(local_8 + 0x72) = *(undefined2 *)(&DAT_00605cae + param_4 * 8);
  *(undefined2 *)(local_8 + 0xb0) = *(undefined2 *)(&DAT_00605ca8 + param_4 * 8);
  *(undefined2 *)(local_8 + 0xb2) = *(undefined2 *)(&DAT_00605caa + param_4 * 8);
  *(short *)(local_8 + 0xb4) = *(short *)(&DAT_00605ca8 + param_4 * 8) + *(short *)(local_8 + 0x70);
  *(short *)(local_8 + 0xb6) = *(short *)(&DAT_00605caa + param_4 * 8) + *(short *)(local_8 + 0x72);
  FUN__text__004079c0(param_2,param_3);
  *(undefined2 *)(local_8 + 0xa8) = 100;
  *(undefined2 *)(local_8 + 0xaa) = 100;
  local_8 = 0x4478d5;
  FUN__text__0056ce80();
  return;
}

