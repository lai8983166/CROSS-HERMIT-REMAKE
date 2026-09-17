
void __thiscall
FUN__text__00499c90(int param_1,undefined1 param_2,undefined2 param_3,undefined2 param_4,
                   undefined1 param_5,undefined1 param_6,undefined1 param_7)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined1 *local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (undefined1 *)(param_1 + 0x108b3e);
  local_8 = param_1;
  _memset(local_c,0,0x10);
  *local_c = param_2;
  *(undefined2 *)(local_c + 2) = param_3;
  *(undefined2 *)(local_c + 4) = param_4;
  local_c[6] = param_5;
  local_c[8] = param_6;
  local_c[7] = param_7;
  local_c[10] = 1;
  local_c[0xb] = 1;
  local_c[0xc] = 0;
  *(undefined2 *)(local_c + 0xe) = 0;
  local_c[0xd] = 0;
  local_c[9] = 2;
  *(undefined1 *)(local_8 + 0x108b34) = 0;
  *(undefined1 *)(local_8 + 0x108b35) = 0;
  *(undefined1 *)(local_8 + 0x108b36) = 0;
  *(undefined1 *)(local_8 + 0x108b38) = 0;
  *(undefined1 *)(local_8 + 0x108b39) = 0;
  *(undefined1 *)(local_8 + 0x108b3a) = 0;
  *(undefined1 *)(local_8 + 0x108b37) = 0;
  FUN__text__0043b250(1);
  local_8 = 0x499d92;
  FUN__text__0056ce80();
  return;
}

