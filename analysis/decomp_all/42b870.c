
void __thiscall
imagelist_dragdrop(int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                  undefined4 param_5,undefined4 param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 auStack_4c [16];
  undefined4 uStack_c;
  int *piStack_8;
  
  puVar2 = auStack_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 != 0) {
    piStack_8 = param_1;
    (*API_COMCTL32_DLL_ImageList_Draw)(*param_1,param_5,param_2,param_3,param_4,param_6);
    uStack_c = __chkesp();
  }
  piStack_8 = (int *)&UNK_0042b8d8;
  __chkesp();
  return;
}

