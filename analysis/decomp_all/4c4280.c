
undefined4 __thiscall
FUN__text__004c4280(int param_1,undefined4 param_2,int param_3,undefined4 param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [18];
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(int *)(param_1 + 0x9230) = param_3;
  *(int *)(param_1 + 0x9234) = param_3 + 0x14;
  if (*(int *)(param_3 + 0xc) == -1) {
    *(undefined4 *)(param_1 + 0x923c) = 0xffffffff;
    *(undefined1 *)(param_1 + 0x9245) = 0;
  }
  else {
    *(undefined4 *)(param_1 + 0x923c) = *(undefined4 *)(param_3 + 0xc);
    *(undefined1 *)(param_1 + 0x9245) = 1;
  }
  if (*(int *)(param_3 + 0x10) == -1) {
    *(undefined4 *)(param_1 + 0x9240) = 0xffffffff;
    *(undefined1 *)(param_1 + 0x9246) = 0;
  }
  else {
    *(undefined4 *)(param_1 + 0x9240) = *(undefined4 *)(param_3 + 0x10);
    *(undefined1 *)(param_1 + 0x9246) = 1;
  }
  *(uint *)(param_1 + 0x9238) =
       *(uint *)(param_1 + 0x9238) & 0xf0000000 | *(uint *)(param_3 + 8) & 0xfffffff;
  *(uint *)(param_1 + 0x9238) =
       *(uint *)(param_1 + 0x9238) & 0xfffffff | *(uint *)(param_3 + 8) & 0xf0000000;
  if (*(uint *)(param_1 + 0x9238) >> 0x1c == 3) {
    *(undefined1 *)(param_1 + 0x9244) = 0;
  }
  else {
    *(undefined1 *)(param_1 + 0x9244) = 1;
  }
  return param_4;
}

