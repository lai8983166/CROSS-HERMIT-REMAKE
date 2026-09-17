
void __thiscall
stretchblt_wrap(int *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
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
    (*API_GDI32_DLL_SelectObject)(param_1[2],param_1[3]);
    uStack_c = __chkesp();
    (*API_GDI32_DLL_StretchBlt)
              (param_2,param_3,param_4,param_5,param_6,piStack_8[2],0,0,
               *(undefined4 *)(*piStack_8 + 4),*(undefined4 *)(*piStack_8 + 8),0xcc0020);
    __chkesp();
    (*API_GDI32_DLL_SelectObject)(piStack_8[2],uStack_c);
    __chkesp();
  }
  piStack_8 = (int *)&UNK_0042081d;
  __chkesp();
  return;
}

