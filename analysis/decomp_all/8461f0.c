
undefined4 * __thiscall
FUN__text1__008461f0
          (undefined4 param_1,undefined1 param_2,undefined1 param_3,undefined4 param_4,
          undefined4 param_5,int param_6)

{
  undefined4 *puVar1;
  
  puVar1 = (undefined4 *)
           (**(code **)(param_6 + 0x20))(*(undefined4 *)(param_6 + 0x28),1,0x1c,param_1);
  if (puVar1 != (undefined4 *)0x0) {
    *puVar1 = 0;
    *(undefined1 *)(puVar1 + 4) = param_2;
    *(undefined1 *)((int)puVar1 + 0x11) = param_3;
    puVar1[5] = param_4;
    puVar1[6] = param_5;
  }
  return puVar1;
}

