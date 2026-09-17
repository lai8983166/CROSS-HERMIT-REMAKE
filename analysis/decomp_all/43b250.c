
undefined4 __thiscall FUN__text__0043b250(int param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  switch(param_2) {
  case 0:
    *(undefined1 *)(param_1 + 0x26595) = 0;
    *(undefined1 *)(param_1 + 0x26596) = 0;
    *(undefined1 *)(param_1 + 0x26597) = 0;
    *(undefined1 *)(param_1 + 0x26598) = 0;
    break;
  case 1:
    *(undefined1 *)(param_1 + 0x26595) = 1;
    *(undefined1 *)(param_1 + 0x26596) = 1;
    *(undefined1 *)(param_1 + 0x26597) = 1;
    *(undefined1 *)(param_1 + 0x26598) = 1;
    break;
  case 2:
    *(undefined1 *)(param_1 + 0x26595) = 1;
    *(undefined1 *)(param_1 + 0x26596) = 1;
    *(undefined1 *)(param_1 + 0x26597) = 1;
    *(undefined1 *)(param_1 + 0x26598) = 0;
    break;
  case 3:
    *(undefined1 *)(param_1 + 0x26595) = 1;
    *(undefined1 *)(param_1 + 0x26596) = 1;
    *(undefined1 *)(param_1 + 0x26597) = 1;
    *(undefined1 *)(param_1 + 0x26598) = 1;
  }
  return 0;
}

